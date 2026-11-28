"""Load and transform transaction-level CSV data into a sequence database."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class SequenceDatabase:
    """Một cơ sở dữ liệu chuỗi dạng ngang.
    Mỗi khóa là một mã định danh chuỗi (sequence ID). Giá trị tương ứng là một danh sách các tập mục (itemset) được sắp xếp theo thứ tự.
    Một tập mục được biểu diễn dưới dạng frozenset[str].
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
    """Đọc và kiểm tra tính hợp lệ của tệp CSV thô."""

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
    """Làm sạch các hàng giao dịch và xây dựng một SequenceDatabase."""

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
        """Nhóm các giao dịch theo ID trình tự (sequence ID) và sắp xếp chúng theo ID giao dịch (transaction ID).
        Theo quy ước CSV hiện tại, tất cả các mục được lưu trữ trong cùng một ô, phân tách bằng
        `item_separator`. Các mục nằm trong cùng một giao dịch được coi là một tập hợp.
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
    
class SequenceDatabaseManager:
    """Store, retrieve and manage a SequenceDatabase."""

    def __init__(self, database: SequenceDatabase | None = None):
        self.database = database
    def _validate_database(self):
        if self.database is None:
            raise ValueError(
                "Sequence Database has not been initialized."
            )
        
    def build(self, records):
        self.database = DataPreprocessor.to_sequence_database(
            records
        )
        return self.database
    
    def get_database(self):
        self._validate_database()
        return self.database

    def get_sequence(self, sequence_id):
        self._validate_database()
        return self.database.get_sequence(sequence_id)

    def summary(self):
        self._validate_database()
        sequences = self.database.sequences
        lengths = [
            len(sequence)
            for sequence in sequences.values()
        ]
        unique_items = {
            item
            for sequence in sequences.values()
            for itemset in sequence
            for item in itemset
        }
        total_sequences = len(sequences)
        total_transactions = sum(lengths)
        return {
            "total_sequences": total_sequences,
            "total_transactions": total_transactions,
            "total_unique_items": len(unique_items),
            "mean_sequence_length": (
                total_transactions / total_sequences
                if total_sequences else 0
            ),
            "min_sequence_length": min(lengths, default=0),
            "max_sequence_length": max(lengths, default=0)
        }
    def save(self, file_path):
        """Save the sequence database to a CSV file."""
        database = self.get_database()
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open(
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                "sequence_id",
                "transaction_id",
                "items"
            ])
            for sequence_id, sequence in database.sequences.items():
                for transaction_id, itemset in enumerate(sequence, start=1):
                    writer.writerow([
                        sequence_id,
                        transaction_id,
                        ";".join(sorted(itemset))
                    ])
        print(f"Sequence database saved to: {path}")
    def load(self, file_path):
        """Load a CSV file and reconstruct the sequence database."""
        records = DataLoader.load_csv(file_path)
        self.database = DataPreprocessor.to_sequence_database(
            records,
            item_separator=";"
        )
        return self.database




