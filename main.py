import argparse
import sys
import logging
from services.reader import read_employees_from_files
from services.reports import get_report_generator
from services.formatter import format_payout_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate employee reports from CSV files.")
    parser.add_argument("files", nargs="+", help="CSV files with employee data")
    parser.add_argument("--report", required=True, help="Type of report to generate (e.g., payout)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        employees = read_employees_from_files(args.files)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e.filename}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Failed to read files")
        sys.exit(1)

    report_type = args.report
    try:
        generator = get_report_generator(report_type)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    report = generator(employees)
    logger.info(f"Report '{report_type}' generated successfully")
    print(format_payout_report(report))


if __name__ == "__main__":
    main()
