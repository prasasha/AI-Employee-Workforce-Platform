from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.performance import Performance


def analyze_performance(rating: float):

    if rating >= 4.5:
        return {
            "performance_level": "Excellent",
            "recommendation": "Employee can handle more challenging responsibilities."
        }

    elif rating >= 3.5:
        return {
            "performance_level": "Good",
            "recommendation": "Employee is performing well and should maintain consistency."
        }

    elif rating >= 2.5:
        return {
            "performance_level": "Average",
            "recommendation": "Employee needs improvement and additional support."
        }

    else:
        return {
            "performance_level": "Needs Improvement",
            "recommendation": "Employee performance requires immediate attention and support."
        }


def analyze_employee_performance(employee_id: int, db: Session):

    # Find employee
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        return None

    # Get all performance records
    performance_records = db.query(Performance).filter(
        Performance.employee_id == employee_id
    ).all()

    # If no performance records
    if not performance_records:
        return {
            "employee_id": employee.id,
            "employee_name": employee.name,
            "message": "No performance records found for this employee."
        }

    # Calculate average rating
    total_rating = sum(record.rating for record in performance_records)
    average_rating = total_rating / len(performance_records)

    # Get AI analysis
    analysis = analyze_performance(average_rating)

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "total_performance_records": len(performance_records),
        "average_rating": round(average_rating, 2),
        "analysis": analysis
    }