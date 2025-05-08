from typing import Callable, Dict, List

from .payout import generate_payout_report
from .reader import Employee

# Mapping of report types to their corresponding generator functions
_REPORTS: Dict[str, Callable[[List[Employee]], dict]] = {
    "payout": generate_payout_report,
}


def get_report_generator(report_type: str) -> Callable[[List[Employee]], dict]:
    """
    Retrieve a report generator function based on the report type.

    Args:
        report_type (str): The type of report to generate (e.g., "payout").

    Returns:
        Callable[[List[Employee]], dict]: A function that generates the report.

    Raises:
        ValueError: If the report type is unknown.
    """
    if report_type not in _REPORTS:
        raise ValueError(f"Unknown report type: {report_type}")
    return _REPORTS[report_type]
