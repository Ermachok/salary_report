import argparse
import logging
import os
import sys

from services.formatter import format_report
from services.reader import read_employees_from_files
from services.reports import get_report_generator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments for the report generation script.

    Returns:
        argparse.Namespace: Parsed arguments including file paths and report type.
    """
    parser = argparse.ArgumentParser(
        description="Generate employee reports from CSV files."
    )
    parser.add_argument("files", nargs="+", help="CSV files with employee data")
    parser.add_argument(
        "--report", required=True, help="Type of report to generate (e.g., payout)"
    )
    return parser.parse_args()


def main():
    """
    Entry point for the script.

    Validates input files, reads employee data, selects a report generator,
    generates the report, and prints the formatted output.
    """
    args = parse_args()

    valid_files = []
    for path in args.files:
        if os.path.isfile(path):
            valid_files.append(path)
        else:
            logger.warning(f"File not found or is not a file: {path}")

    if not valid_files:
        logger.error("No valid input files provided.")
        sys.exit(1)

    try:
        employees = read_employees_from_files(valid_files)
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
    print(format_report(report_type, report))


if __name__ == "__main__":
    main()
