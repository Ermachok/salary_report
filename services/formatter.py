from typing import Dict, Any

def format_report(report_type: str, data: Dict[str, Any]) -> str:
    """
    Format the report data based on the specified report type.

    Args:
        report_type (str): The type of report to format (e.g., "payout").
        data (Dict[str, Any]): The raw report data to format.

    Returns:
        str: A string representation of the formatted report.

    Raises:
        ValueError: If the report type is unknown.
    """
    if report_type == "payout":
        return format_payout_report(data)
    raise ValueError(f"Unknown report type: {report_type}")


def format_payout_report(data: Dict[str, Any]) -> str:
    """
    Format payout report data into a human-readable string.

    Args:
        data (Dict[str, Any]): A dictionary containing department-wise employee payout info.

    Returns:
        str: A formatted string representing the payout report.
    """
    lines = []

    for department, info in data.items():
        lines.append(f"{department}")
        for emp in info["employees"]:
            name = emp["name"]
            hours = emp["hours_worked"]
            rate = emp["hourly_rate"]
            payout = emp["payout"]
            lines.append(f"{'--------------':<14} {name:<20}\t{hours:<6} {rate:<5} ${payout}")
        lines.append(f"{'':>45}{info['total_hours']:<8} ${info['total_payout']}")
        lines.append("")

    return "\n".join(lines)
