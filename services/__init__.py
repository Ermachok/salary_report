from .payout import generate_payout_report


def get_report_generator(name: str):
    if name == "payout":
        return generate_payout_report
    raise ValueError(f"Unknown report type: {name}")
