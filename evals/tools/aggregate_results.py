#!/usr/bin/env python3
"""Aggregate per-run grading and timing files into an iteration benchmark.

``tool_calls`` and ``errors`` cannot be recovered from the available grading
and timing artifacts.  They are therefore emitted as null and require manual
post-processing if those measurements are needed.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


CONFIGURATIONS = ("with_skill", "without_skill")
METRICS = ("pass_rate", "time_seconds", "tokens")


class AggregationError(Exception):
    """Raised when an iteration directory does not contain usable artifacts."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise AggregationError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise AggregationError(f"expected a JSON object in {path}")
    return value


def _number(value: Any, label: str, path: Path) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AggregationError(f"{path}: {label} must be a number")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise AggregationError(f"{path}: {label} must be finite")
    return numeric


def _integer(value: Any, label: str, path: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise AggregationError(f"{path}: {label} must be an integer")
    return value


def _configuration_and_artifact_dir(
    metadata_path: Path, iteration_dir: Path
) -> tuple[str, Path]:
    """Find a configuration that is an ancestor of metadata_path.

    This is the configuration-first compatibility path.  The native layout is
    handled by _runs_from_metadata, where configuration directories are
    children of the metadata directory.
    """
    relative_parts = metadata_path.relative_to(iteration_dir).parts[:-1]
    indexes = [index for index, part in enumerate(relative_parts) if part in CONFIGURATIONS]
    if len(indexes) != 1:
        raise AggregationError(
            f"{metadata_path}: expected exactly one configuration directory "
            f"({', '.join(CONFIGURATIONS)})"
        )
    index = indexes[0]
    configuration = relative_parts[index]
    configuration_dir = iteration_dir.joinpath(*relative_parts[: index + 1])
    candidates = [metadata_path.parent, configuration_dir]
    artifact_dirs = [
        candidate
        for candidate in candidates
        if (candidate / "grading.json").is_file() and (candidate / "timing.json").is_file()
    ]
    if len(artifact_dirs) != 1:
        raise AggregationError(
            f"{metadata_path}: could not identify one grading/timing directory for {configuration}"
        )
    return configuration, artifact_dirs[0]


def _run_from_metadata(
    metadata_path: Path, configuration: str, artifact_dir: Path
) -> dict[str, Any]:
    grading_path = artifact_dir / "grading.json"
    timing_path = artifact_dir / "timing.json"

    metadata = _read_json(metadata_path)
    grading = _read_json(grading_path)
    timing = _read_json(timing_path)
    summary = grading.get("summary")
    if not isinstance(summary, dict):
        raise AggregationError(f"{grading_path}: summary must be an object")
    expectations = grading.get("expectations")
    if not isinstance(expectations, list):
        raise AggregationError(f"{grading_path}: expectations must be an array")

    eval_id = metadata.get("eval_id")
    if isinstance(eval_id, bool) or not isinstance(eval_id, (int, str)):
        raise AggregationError(f"{metadata_path}: eval_id must be an integer or string")
    eval_name = metadata.get("eval_name")
    if not isinstance(eval_name, str) or not eval_name:
        raise AggregationError(f"{metadata_path}: eval_name must be a non-empty string")

    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "configuration": configuration,
        "run_number": 1,
        "result": {
            "pass_rate": _number(summary.get("pass_rate"), "summary.pass_rate", grading_path),
            "passed": _integer(summary.get("passed"), "summary.passed", grading_path),
            "failed": _integer(summary.get("failed"), "summary.failed", grading_path),
            "total": _integer(summary.get("total"), "summary.total", grading_path),
            "time_seconds": _number(
                timing.get("total_duration_seconds"), "total_duration_seconds", timing_path
            ),
            "tokens": _integer(timing.get("total_tokens"), "total_tokens", timing_path),
            "tool_calls": None,
            "errors": None,
        },
        "expectations": expectations,
        "notes": [],
    }


def _runs_from_metadata(metadata_path: Path, iteration_dir: Path) -> list[dict[str, Any]]:
    """Read both supported layouts without inferring names from directories."""
    child_configurations = [
        (configuration, metadata_path.parent / configuration)
        for configuration in CONFIGURATIONS
        if (metadata_path.parent / configuration).is_dir()
    ]
    if child_configurations:
        if len(child_configurations) != len(CONFIGURATIONS):
            found = ", ".join(configuration for configuration, _ in child_configurations)
            raise AggregationError(
                f"{metadata_path.parent}: expected both configurations; found {found}"
            )
        runs = []
        for configuration, artifact_dir in child_configurations:
            if not (artifact_dir / "grading.json").is_file() or not (artifact_dir / "timing.json").is_file():
                raise AggregationError(
                    f"{artifact_dir}: requires grading.json and timing.json"
                )
            runs.append(_run_from_metadata(metadata_path, configuration, artifact_dir))
        return runs

    configuration, artifact_dir = _configuration_and_artifact_dir(metadata_path, iteration_dir)
    return [_run_from_metadata(metadata_path, configuration, artifact_dir)]


def _sort_key(run: dict[str, Any]) -> tuple[int, Any, str]:
    eval_id = run["eval_id"]
    if isinstance(eval_id, int):
        return (0, eval_id, run["eval_name"])
    return (1, eval_id, run["eval_name"])


def _metric_summary(values: list[float]) -> dict[str, float]:
    if not values:
        raise AggregationError("cannot summarize an empty configuration")
    return {
        "mean": statistics.fmean(values),
        "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def _build_document(iteration_dir: Path) -> dict[str, Any]:
    runs_by_configuration: dict[str, list[dict[str, Any]]] = {
        configuration: [] for configuration in CONFIGURATIONS
    }
    for metadata_path in iteration_dir.rglob("eval_metadata.json"):
        for run in _runs_from_metadata(metadata_path, iteration_dir):
            runs_by_configuration[run["configuration"]].append(run)

    for configuration, runs in runs_by_configuration.items():
        if not runs:
            raise AggregationError(
                f"{iteration_dir}: no eval_metadata.json found for {configuration}"
            )
        runs.sort(key=_sort_key)

    runs = [run for configuration in CONFIGURATIONS for run in runs_by_configuration[configuration]]
    summaries: dict[str, dict[str, dict[str, float]]] = {}
    for configuration, configuration_runs in runs_by_configuration.items():
        summaries[configuration] = {
            metric: _metric_summary(
                [_number(run["result"][metric], metric, iteration_dir) for run in configuration_runs]
            )
            for metric in METRICS
        }

    delta = {
        metric: f"{summaries['with_skill'][metric]['mean'] - summaries['without_skill'][metric]['mean']:+.2f}"
        for metric in METRICS
    }
    eval_ids = sorted({run["eval_id"] for run in runs}, key=lambda item: (isinstance(item, str), item))
    return {
        "metadata": {
            "skill_name": None,
            "skill_path": None,
            "executor_model": None,
            "analyzer_model": None,
            "timestamp": None,
            "evals_run": eval_ids,
            "runs_per_configuration": 1,
            "note_on_runs_per_configuration": None,
        },
        "runs": runs,
        "run_summary": {**summaries, "delta": delta},
        "notes": [],
    }


def _write_document(path: Path, document: dict[str, Any]) -> None:
    temporary_path = path.with_name(f".{path.name}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary_path.replace(path)
    except OSError as error:
        raise AggregationError(f"cannot write {path}: {error}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate iteration grading.json and timing.json files into benchmark.json."
    )
    parser.add_argument("iteration_dir", type=Path, help="Directory containing evaluation artifacts")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing benchmark.json")
    arguments = parser.parse_args(argv)

    iteration_dir = arguments.iteration_dir.resolve()
    if not iteration_dir.is_dir():
        print(f"error: iteration directory does not exist: {iteration_dir}", file=sys.stderr)
        return 2
    output_path = iteration_dir / "benchmark.json"
    if output_path.exists() and not arguments.force:
        print(
            f"warning: {output_path} already exists; use --force to overwrite it",
            file=sys.stderr,
        )
        return 1
    try:
        document = _build_document(iteration_dir)
        _write_document(output_path, document)
    except AggregationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
