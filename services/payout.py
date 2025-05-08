from collections import defaultdict
from typing import List, Dict, Any
from .reader import Employee


def generate_payout_report(employees: List[Employee]) -> Dict[str, Any]:
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
