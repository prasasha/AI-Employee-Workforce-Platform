from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance


def generate_workforce_insights(db: Session):

    employees = db.query(Employee).all()
    tasks = db.query(Task).all()
    performance_records = db.query(Performance).all()

    total_employees = len(employees)
    total_tasks = len(tasks)

    # Calculate workforce average performance
    if performance_records:
        average_performance = (
            sum(record.rating for record in performance_records)
            / len(performance_records)
        )
        average_performance = round(average_performance, 2)
    else:
        average_performance = 0

    # Find high-performing employees
    high_performers = []

    for employee in employees:
        employee_records = [
            record for record in performance_records
            if record.employee_id == employee.id
        ]

        if employee_records:
            average_rating = (
                sum(record.rating for record in employee_records)
                / len(employee_records)
            )

            if average_rating >= 4.5:
                high_performers.append({
                    "employee_id": employee.id,
                    "employee_name": employee.name,
                    "average_rating": round(average_rating, 2)
                })

    return {
        "total_employees": total_employees,
        "total_tasks": total_tasks,
        "average_workforce_performance": average_performance,
        "high_performers": high_performers
    }