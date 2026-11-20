"""Load and transform transaction-level CSV data into a sequence database."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class SequenceDatabase:
    """A horizontal sequence database.

    Each key is a sequence ID. Its value is an ordered list of itemsets.
    An itemset is represented as a frozenset[str].
    """

    sequences: dict[str, tuple[frozenset[str], ...]]

    def __len__(self) -> int:
        """Return the number of data sequences."""
        return len(self.sequences)

    def get_sequence_ids(self) -> list[str]:
        """Return sequence IDs in their stored order."""
        return list(self.sequences.keys())

    def to_list(self) -> list[tuple[frozenset[str], ...]]:
        """Return the database sequences as a list."""
        return list(self.sequences.values())


class DataLoader:
    """Read and validate the raw CSV file."""

    REQUIRED_COLUMNS = {"sequence_id", "transaction_id", "items"}

    @staticmethod
    def load_csv(file_path: str | Path) -> list[dict[str, str]]:
        """Load rows from CSV and validate the required column names."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            columns = set(reader.fieldnames or [])
            missing = DataLoader.REQUIRED_COLUMNS - columns
            if missing:
                raise ValueError(f"Missing required CSV columns: {sorted(missing)}")
            return list(reader)


class DataPreprocessor:
    """Clean transaction rows and build a SequenceDatabase."""

    @staticmethod
    def _transaction_sort_key(value: str):
        """Sort numeric transaction IDs numerically, otherwise lexically."""
        try:
            return (0, float(value))
        except (TypeError, ValueError):
            return (1, str(value))

    @classmethod
    def to_sequence_database(
        cls,
        records: Iterable[dict[str, str]],
        item_separator: str = ";",
    ) -> SequenceDatabase:
        """Group transactions by sequence ID and order them by transaction ID.

        The current CSV convention stores all items in one cell, separated by
        `item_separator`. Items within one transaction are treated as a set.
        """
        grouped: dict[str, list[tuple[str, frozenset[str]]]] = {}

        for row_number, row in enumerate(records, start=2):
            sequence_id = str(row.get("sequence_id", "")).strip()
            transaction_id = str(row.get("transaction_id", "")).strip()
            raw_items = str(row.get("items", "")).strip()

            if not sequence_id or not transaction_id:
                raise ValueError(
                    f"Empty sequence_id or transaction_id at CSV row {row_number}"
                )

            items = frozenset(
                item.strip()
                for item in raw_items.split(item_separator)
                if item.strip()
            )
            if not items:
                raise ValueError(f"No valid items at CSV row {row_number}")

            grouped.setdefault(sequence_id, []).append((transaction_id, items))

        sequences: dict[str, tuple[frozenset[str], ...]] = {}
        for sequence_id, transactions in grouped.items():
            transactions.sort(key=lambda pair: cls._transaction_sort_key(pair[0]))
            sequences[sequence_id] = tuple(items for _, items in transactions)

        return SequenceDatabase(sequences=sequences)
