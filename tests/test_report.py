import pytest
from services.formatter import format_report
from services.payout import generate_payout_report
from services.reader import read_employees_from_files


@pytest.fixture
def make_csv(tmp_path):
    """
    Фикстура для создания CSV-файлов с заданным содержимым.
    """

    def _make(content: str):
        path = tmp_path / "file.csv"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return _make


@pytest.fixture
def sample_csv_file(make_csv):
    csv_content = (
        "id,email,name,department,hours_worked,hourly_rate\n"
        "1,john@example.com,John Doe,Engineering,40,25\n"
        "2,jane@example.com,Jane Smith,Engineering,35,30\n"
    )
    return make_csv(csv_content)


def test_read_employees_from_files(sample_csv_file):
    employees = read_employees_from_files([sample_csv_file])
    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].hourly_rate == 30


def test_generate_payout_report_contains_department(sample_csv_file):
    employees = read_employees_from_files([sample_csv_file])
    report = generate_payout_report(employees)
    assert "Engineering" in report


def test_generate_payout_report_totals_are_correct(sample_csv_file):
    employees = read_employees_from_files([sample_csv_file])
    report = generate_payout_report(employees)
    dept = report["Engineering"]

    expected_total_hours = 40 + 35
    expected_total_payout = 40 * 25 + 35 * 30

    assert dept["total_hours"] == expected_total_hours
    assert dept["total_payout"] == expected_total_payout


def test_format_report_output(sample_csv_file):
    employees = read_employees_from_files([sample_csv_file])
    report = generate_payout_report(employees)
    formatted = format_report("payout", report)

    assert "Engineering" in formatted
    assert "John Doe" in formatted
    assert "Total hours:" in formatted
    assert "$1000" in formatted


def test_read_employees_from_files_invalid_path():
    with pytest.raises(FileNotFoundError):
        read_employees_from_files(["non_existing.csv"])


def test_read_employees_missing_rate_field(make_csv):
    csv_content = (
        "id,email,name,department,hours_worked\n"
        "1,john@example.com,John Doe,Engineering,40\n"
    )
    file_path = make_csv(csv_content)

    with pytest.raises(ValueError, match="Missing rate column"):
        read_employees_from_files([file_path])


def test_read_employees_malformed_row(make_csv, caplog):
    csv_content = (
        "id,email,name,department,hours_worked,hourly_rate\n"
        "oops,wrong@example.com,Broken,HR,badnumber,rate\n"
    )
    file_path = make_csv(csv_content)

    employees = read_employees_from_files([file_path])
    assert len(employees) == 0
    assert "Skipping malformed row" in caplog.text


def test_format_report_invalid_type():
    with pytest.raises(ValueError):
        format_report("unknown", {})
