from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance


def calculate_role_match_score(
    employee_role: str,
    task_requirement: str
):
    employee_role = employee_role.lower()
    task_requirement = task_requirement.lower()

    role_keywords = {
        "frontend developer": [
            "react",
            "frontend",
            "javascript",
            "html",
            "css",
            "ui"
        ],
        "backend developer": [
            "backend",
            "python",
            "fastapi",
            "api",
            "database",
            "sql"
        ],
        "ui designer": [
            "figma",
            "design",
            "ui",
            "ux",
            "prototype"
        ],
        "full stack developer": [
            "frontend",
            "backend",
            "react",
            "python",
            "fastapi",
            "api"
        ]
    }

    # Direct role matching
    if employee_role in task_requirement:
        return 20

    # Keyword matching
    keywords = role_keywords.get(employee_role, [])

    for keyword in keywords:
        if keyword in task_requirement:
            return 20

    return 0


def calculate_recommendation_score(
    average_rating: float,
    current_workload: int,
    employee_role: str,
    task_requirement: str
):
    # Performance score - maximum 50 points
    performance_score = (average_rating / 5) * 50

    # Workload score - maximum 30 points
    if current_workload == 0:
        workload_score = 30
    elif current_workload <= 2:
        workload_score = 20
    elif current_workload <= 5:
        workload_score = 10
    else:
        workload_score = 0

    # Role / skill matching - maximum 20 points
    role_score = calculate_role_match_score(
        employee_role,
        task_requirement
    )

    total_score = (
        performance_score
        + workload_score
        + role_score
    )

    return round(total_score, 2)


def generate_recommendation_reason(
    average_rating: float,
    current_workload: int,
    employee_role: str,
    task_requirement: str
):
    reasons = []

    if average_rating >= 4.5:
        reasons.append("Excellent performance rating")
    elif average_rating >= 3.5:
        reasons.append("Good performance rating")

    if current_workload == 0:
        reasons.append("Currently has no assigned tasks")
    elif current_workload <= 2:
        reasons.append("Has a low current workload")

    role_score = calculate_role_match_score(
        employee_role,
        task_requirement
    )

    if role_score > 0:
        reasons.append(
            "Employee role and skills match the task requirements"
        )

    if not reasons:
        reasons.append(
            "Employee was selected based on the overall recommendation score"
        )

    return reasons


def calculate_confidence_score(
    recommendation_score: float
):
    # Recommendation score is already out of 100
    confidence_score = recommendation_score

    if confidence_score >= 80:
        confidence_level = "High"
    elif confidence_score >= 60:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"

    return {
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level
    }


def recommend_best_employee(
    task_requirement: str,
    db: Session
):
    employees = db.query(Employee).all()

    recommendations = []

    for employee in employees:

        # Get performance records
        performance_records = db.query(Performance).filter(
            Performance.employee_id == employee.id
        ).all()

        # Calculate average performance
        if performance_records:
            average_rating = (
                sum(record.rating for record in performance_records)
                / len(performance_records)
            )
        else:
            average_rating = 0

        # Calculate current workload
        current_workload = db.query(Task).filter(
            Task.employee_id == employee.id
        ).count()

        # Calculate recommendation score
        recommendation_score = calculate_recommendation_score(
            average_rating=average_rating,
            current_workload=current_workload,
            employee_role=employee.role,
            task_requirement=task_requirement
        )

        # Generate recommendation explanation
        recommendation_reason = generate_recommendation_reason(
            average_rating=average_rating,
            current_workload=current_workload,
            employee_role=employee.role,
            task_requirement=task_requirement
        )

        # Calculate confidence
        confidence = calculate_confidence_score(
            recommendation_score
        )

        recommendations.append({
            "employee_id": employee.id,
            "employee_name": employee.name,
            "employee_role": employee.role,
            "average_rating": round(average_rating, 2),
            "current_workload": current_workload,
            "recommendation_score": recommendation_score,
            "recommendation_reason": recommendation_reason,
            "confidence": confidence
        })

    # Highest score first
    recommendations.sort(
        key=lambda employee: employee["recommendation_score"],
        reverse=True
    )

    # No employees found
    if not recommendations:
        return {
            "message": "No employees found"
        }

    # Best recommendation
    best_employee = recommendations[0]

    return {
        "task_requirement": task_requirement,
        "best_recommendation": best_employee,
        "all_recommendations": recommendations
    }