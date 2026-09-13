import os
import json

from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance

from app.services.ai_task_recommendation_service import (
    recommend_best_employee
)


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# GEMINI MODEL
# ==========================================

MODEL_NAME = "gemini-3.6-flash"


# ==========================================
# GET COMPLETE WORKFORCE CONTEXT
# ==========================================

def get_workforce_context(db: Session):

    employees = db.query(Employee).all()
    tasks = db.query(Task).all()
    performance_records = db.query(Performance).all()

    employee_data = []

    for employee in employees:

        employee_tasks = [
            task for task in tasks
            if task.employee_id == employee.id
        ]

        employee_performance = [
            record for record in performance_records
            if record.employee_id == employee.id
        ]

        if employee_performance:
            average_rating = (
                sum(record.rating for record in employee_performance)
                / len(employee_performance)
            )
        else:
            average_rating = 0

        employee_data.append({
            "id": employee.id,
            "name": employee.name,
            "role": employee.role,
            "department": employee.department,
            "status": employee.status,
            "total_tasks": len(employee_tasks),
            "average_performance": round(average_rating, 2)
        })

    return {
        "total_employees": len(employees),
        "total_tasks": len(tasks),
        "employees": employee_data
    }


# ==========================================
# RAG-STYLE CONTEXT RETRIEVAL
# ==========================================

def get_relevant_workforce_context(question: str, db: Session):

    workforce_context = get_workforce_context(db)

    question_lower = question.lower()
    question_words = question_lower.split()

    relevant_employees = []

    for employee in workforce_context["employees"]:

        employee_text = (
            f"{employee['name']} "
            f"{employee['role']} "
            f"{employee['department']} "
            f"{employee['status']}"
        ).lower()

        if any(
            word in employee_text
            for word in question_words
            if len(word) > 2
        ):
            relevant_employees.append(employee)

    if not relevant_employees:

        return workforce_context

    return {
        "total_employees": workforce_context["total_employees"],
        "total_tasks": workforce_context["total_tasks"],
        "relevant_employees": relevant_employees
    }


# ==========================================
# SAFE JSON RESPONSE
# ==========================================

def generate_structured_response(prompt: str):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    response_text = response.text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:

        return {
            "summary": response_text,
            "performance_analysis": "Not available",
            "workload_analysis": "Not available",
            "risk_level": "Not available",
            "recommendations": []
        }


# ==========================================
# GEMINI AI WORKFORCE ASSISTANT
# ==========================================

def process_workforce_question(question: str, db: Session):

    relevant_context = get_relevant_workforce_context(
        question,
        db
    )

    prompt = f"""
You are an AI Workforce Assistant.

Answer the user's question using ONLY the retrieved workforce data.

RETRIEVED WORKFORCE DATA:
{relevant_context}

USER QUESTION:
{question}

Return ONLY valid JSON.

Use exactly this format:

{{
    "summary": "short direct answer",
    "performance_analysis": "performance details",
    "workload_analysis": "workload details",
    "risk_level": "Low, Medium, High, or Not Available",
    "recommendations": [
        "recommendation 1",
        "recommendation 2"
    ]
}}

Rules:
- Use only the provided workforce data.
- Do not invent information.
- If data is unavailable, say "Not Available".
"""

    try:
        return generate_structured_response(prompt)

    except Exception as error:

        return {
            "summary": f"AI Assistant Error: {str(error)}",
            "performance_analysis": "Not available",
            "workload_analysis": "Not available",
            "risk_level": "Not available",
            "recommendations": []
        }


# ==========================================
# GEMINI AI WORKFORCE INSIGHTS
# ==========================================

def generate_ai_workforce_insights(db: Session):

    workforce_context = get_workforce_context(db)

    prompt = f"""
You are an AI Workforce Analyst.

Analyze this workforce data:

{workforce_context}

Return ONLY valid JSON in this format:

{{
    "workforce_summary": "summary",
    "performance_analysis": "analysis",
    "workload_analysis": "analysis",
    "top_performers": [],
    "potential_issues": [],
    "recommendations": []
}}

Use only the provided data.
Do not invent information.
"""

    try:
        return generate_structured_response(prompt)

    except Exception as error:

        return {
            "workforce_summary": f"AI Error: {str(error)}",
            "performance_analysis": "",
            "workload_analysis": "",
            "top_performers": [],
            "potential_issues": [],
            "recommendations": []
        }


# ==========================================
# AI SMART TASK ASSIGNMENT
# ==========================================

def generate_smart_task_assignment(
    task_requirement: str,
    db: Session
):

    recommendation_result = recommend_best_employee(
        task_requirement=task_requirement,
        db=db
    )

    workforce_context = get_workforce_context(db)

    if (
        isinstance(recommendation_result, dict)
        and recommendation_result.get("message") == "No employees found"
    ):
        return recommendation_result

    best_employee = recommendation_result.get(
        "best_recommendation"
    )

    prompt = f"""
You are an AI Task Assignment Assistant.

TASK REQUIREMENT:
{task_requirement}

WORKFORCE DATA:
{workforce_context}

ALGORITHM RECOMMENDATION:
{best_employee}

Return ONLY valid JSON:

{{
    "recommended_employee": "employee name or Not Available",
    "suitability_reason": "reason",
    "performance_analysis": "analysis",
    "workload_analysis": "analysis",
    "role_relevance": "analysis",
    "final_recommendation": "final recommendation"
}}

Use only provided data.
Do not invent employee skills.
"""

    try:

        ai_analysis = generate_structured_response(prompt)

        return {
            "task_requirement": task_requirement,
            "algorithm_recommendation": best_employee,
            "ai_assignment_analysis": ai_analysis
        }

    except Exception as error:

        return {
            "task_requirement": task_requirement,
            "algorithm_recommendation": best_employee,
            "ai_assignment_analysis": {
                "error": str(error)
            }
        }


# ==========================================
# AI EMPLOYEE RISK CALCULATION
# ==========================================

def calculate_employee_risk(
    average_performance: float,
    total_tasks: int
):

    risk_score = 0
    risk_reasons = []

    if average_performance < 2.5:
        risk_score += 60
        risk_reasons.append("Low performance rating")

    elif average_performance < 3.5:
        risk_score += 30
        risk_reasons.append("Moderate performance rating")

    if total_tasks >= 6:
        risk_score += 40
        risk_reasons.append("Very high workload")

    elif total_tasks >= 4:
        risk_score += 20
        risk_reasons.append("High workload")

    if risk_score >= 60:
        risk_level = "High"

    elif risk_score >= 30:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": risk_reasons
    }


# ==========================================
# AI EMPLOYEE RISK PREDICTION
# ==========================================

def generate_employee_risk_prediction(db: Session):

    workforce_context = get_workforce_context(db)

    employee_risk_data = []

    for employee in workforce_context["employees"]:

        risk_result = calculate_employee_risk(
            average_performance=employee["average_performance"],
            total_tasks=employee["total_tasks"]
        )

        employee_risk_data.append({
            "employee_id": employee["id"],
            "employee_name": employee["name"],
            "employee_role": employee["role"],
            "average_performance": employee["average_performance"],
            "total_tasks": employee["total_tasks"],
            "risk_score": risk_result["risk_score"],
            "risk_level": risk_result["risk_level"],
            "risk_reasons": risk_result["risk_reasons"]
        })

    employee_risk_data.sort(
        key=lambda employee: employee["risk_score"],
        reverse=True
    )

    prompt = f"""
You are an AI Workforce Risk Analyst.

EMPLOYEE RISK DATA:
{employee_risk_data}

Return ONLY valid JSON:

{{
    "overall_risk_summary": "summary",
    "high_risk_employees": [],
    "medium_risk_employees": [],
    "low_risk_employees": [],
    "main_risk_factors": [],
    "recommended_actions": []
}}

Use only the provided data.
"""

    try:

        ai_analysis = generate_structured_response(prompt)

        return {
            "employee_risk_predictions": employee_risk_data,
            "ai_risk_analysis": ai_analysis
        }

    except Exception as error:

        return {
            "employee_risk_predictions": employee_risk_data,
            "ai_risk_analysis": {
                "error": str(error)
            }
        }