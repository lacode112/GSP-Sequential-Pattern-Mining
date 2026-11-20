"""Run experiments and summarize GSP results."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Iterable

from data_processing import SequenceDatabase
from gsp import GSP


@dataclass
class ExperimentResult:
    min_support: int | float
    runtime_seconds: float
    number_of_patterns: int


class ExperimentRunner:
    """Run GSP under different parameter configurations."""

    def __init__(self, algorithm: GSP | None = None) -> None:
        self.algorithm = algorithm or GSP()

    def run_one(
        self,
        database: SequenceDatabase,
        min_support: int | float,
    ) -> tuple[dict, ExperimentResult]:
        """Run one configuration and record runtime and pattern count."""
        start = perf_counter()
        patterns = self.algorithm.fit(database, min_support)
        runtime = perf_counter() - start

        result = ExperimentResult(
            min_support=min_support,
            runtime_seconds=runtime,
            number_of_patterns=len(patterns),
        )
        return patterns, result

    def run_many(
        self,
        database: SequenceDatabase,
        min_support_values: Iterable[int | float],
    ) -> list[tuple[dict, ExperimentResult]]:
        """Run the algorithm for each supplied MinSup value."""
        # TODO: call run_one for every value and collect the outputs.
        raise NotImplementedError("Batch experiments have not been implemented.")


class ExperimentAnalyzer:
    """Prepare summaries and observations from experiment outputs."""

    @staticmethod
    def to_records(results: Iterable[ExperimentResult]) -> list[dict]:
        """Convert experiment results to records suitable for CSV export."""
        return [
            {
                "min_support": result.min_support,
                "runtime_seconds": result.runtime_seconds,
                "number_of_patterns": result.number_of_patterns,
            }
            for result in results
        ]


class LibraryComparator:
    """Optional: compare the custom implementation with an external library."""

    def compare(self, custom_results: dict, library_results: dict) -> dict:
        """Compare pattern sets and, if available, execution times.

        TODO: normalize both libraries' output representations before
        comparing pattern identity and support values.
        """
        raise NotImplementedError("Library comparison is optional and not implemented.")
