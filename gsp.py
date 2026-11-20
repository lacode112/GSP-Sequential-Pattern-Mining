"""Core components for the GSP sequential pattern mining algorithm.

Representation convention:
    Sequence = tuple[frozenset[str], ...]
    Itemset  = frozenset[str]

The group should implement and test the TODO methods below. Keep support
counting at the data-sequence level: one sequence contributes at most one
count to a pattern, even if the pattern occurs multiple times in that sequence.
"""

from __future__ import annotations

from typing import Iterable

from data_processing import SequenceDatabase

Itemset = frozenset[str]
Sequence = tuple[Itemset, ...]


class CandidateGenerator:
    """Generate candidate (k+1)-sequences from frequent k-sequences."""

    def generate(
        self,
        frequent_sequences: Iterable[Sequence],
        frequent_items: Iterable[str],
    ) -> set[Sequence]:
        """Generate candidates using i-extension and s-extension.

        TODO:
        1. Implement i-extension: append an item to the final itemset while
           preserving the agreed item ordering.
        2. Implement s-extension: append a new singleton itemset.
        3. Avoid duplicate candidates.
        """
        raise NotImplementedError("Candidate generation has not been implemented.")


class CandidatePruner:
    """Prune candidates that violate the Apriori property."""

    def prune(
        self,
        candidates: Iterable[Sequence],
        frequent_sequences: set[Sequence],
    ) -> set[Sequence]:
        """Keep candidates whose required immediate subsequences are frequent.

        TODO:
        1. Generate all immediate subsequences by removing one item.
        2. If an itemset becomes empty, remove that itemset from the sequence.
        3. Remove a candidate if any required (k)-subsequence is infrequent.
        """
        raise NotImplementedError("Candidate pruning has not been implemented.")


class SupportCounter:
    """Check subsequence containment and count candidate support."""

    @staticmethod
    def is_subsequence(pattern: Sequence, data_sequence: Sequence) -> bool:
        """Return True if every pattern itemset is contained in order.

        TODO: implement an ordered subsequence check. A pattern itemset must
        be a subset of a matched data itemset.
        """
        raise NotImplementedError("Subsequence checking has not been implemented.")

    def count_support(
        self,
        candidate: Sequence,
        database: SequenceDatabase,
    ) -> int:
        """Count how many distinct data sequences contain the candidate.

        TODO: count each sequence ID no more than once.
        """
        raise NotImplementedError("Support counting has not been implemented.")


class GSP:
    """Coordinate the level-wise GSP mining process."""

    def __init__(self) -> None:
        self.generator = CandidateGenerator()
        self.pruner = CandidatePruner()
        self.counter = SupportCounter()

    def fit(
        self,
        database: SequenceDatabase,
        min_support: int | float,
    ) -> dict[Sequence, int]:
        """Mine and return {frequent_sequence: absolute_support}.

        TODO:
        1. Convert relative MinSup (0 < float <= 1) to an absolute threshold,
           if the group chooses to support relative thresholds.
        2. Count frequent 1-sequences.
        3. Iteratively generate, prune, and count candidates of length k+1.
        4. Stop when no frequent candidates remain.
        5. Return all frequent sequences and their absolute support counts.

        Document clearly whether the public API accepts absolute support,
        relative support, or both.
        """
        raise NotImplementedError("The GSP algorithm has not been implemented.")
