import logging
from dataclasses import dataclass
from typing import List
from config import RATE_FIELDS

logger = logging.getLogger(__name__)


@dataclass
class Employee:
    """
    Data class representing an employee record.
    """
    id: int
    email: str
    name: str
    department: str
    hours_worked: int
    hourly_rate: int


def read_employees_from_files(file_paths: List[str]) -> List[Employee]:
    """
    Read and parse employee data from a list of CSV files.

    Args:
        file_paths (List[str]): A list of paths to CSV files containing employee data.

    Returns:
        List[Employee]: A list of Employee objects parsed from the provided files.

    Raises:
        ValueError: If a required rate field is missing from any file.
    """
    all_employees = []

    for path in file_paths:
        with open(path, encoding="utf-8") as f:
            header = f.readline().strip().split(",")
            header = [h.strip() for h in header]
            logger.debug(f"Parsed header from {path}: {header}")

            rate_field = next((h for h in header if h in RATE_FIELDS), None)
            if not rate_field:
                raise ValueError(f"Missing rate column in file: {path}")

            for line in f:
                if not line.strip():
                    continue
                values = [v.strip() for v in line.strip().split(",")]
                row = dict(zip(header, values))
                try:
                    employee = Employee(
                        id=int(row["id"]),
                        email=row["email"],
                        name=row["name"],
                        department=row["department"],
                        hours_worked=int(row["hours_worked"]),
                        hourly_rate=int(row[rate_field]),
                    )
                    all_employees.append(employee)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Skipping malformed row in {path}: {row} ({e})")

    return all_employees
