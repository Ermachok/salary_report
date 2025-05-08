from typing import Callable, Dict, List
from .payout import generate_payout_report
from .reader import Employee

_REPORTS: Dict[str, Callable[[List[Employee]], dict]] = {
    "payout": generate_payout_report,

}


def get_report_generator(report_type: str) -> Callable[[List[Employee]], dict]:
    if report_type not in _REPORTS:
        raise ValueError(f"Unknown report type: {report_type}")
    return _REPORTS[report_type]
