from collections import defaultdict
from typing import List, Dict, Any
from .reader import Employee


def generate_payout_report(employees: List[Employee]) -> Dict[str, Any]:
    """
    Generate a payout report for a list of employees, grouped by department.

    Args:
        employees (List[Employee]): A list of Employee objects.

    Returns:
        Dict[str, Any]: A dictionary where each key is a department name and the value is:
                        - a list of employees with their hours, rates, and payouts,
                        - total hours worked for the department,
                        - total payout amount for the department.
    """
    report = {}
    departments = defaultdict(list)

    for emp in employees:
        payout = emp.hours_worked * emp.hourly_rate
        emp_dict = {
            "name": emp.name,
            "hours_worked": emp.hours_worked,
            "hourly_rate": emp.hourly_rate,
            "payout": payout
        }
        departments[emp.department].append(emp_dict)

    for dept, emps in departments.items():
        total_hours = sum(e["hours_worked"] for e in emps)
        total_payout = sum(e["payout"] for e in emps)
        report[dept] = {
            "employees": emps,
            "total_hours": total_hours,
            "total_payout": total_payout,
        }

    return report
