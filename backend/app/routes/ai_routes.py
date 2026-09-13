from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import os 
 
from dotenv import load_dotenv 
from google import genai 
 
from app.database.database import get_db 
from app.models.employee import Employee 
from app.models.task import Task 
from app.models.performance import Performance 
 
 
# Load environment variables from .env 
load_dotenv() 
 
 
router = APIRouter( 
    prefix="/ai", 
    tags=["AI Workforce"] 
) 
 
 
# ============================================================ 
# GEMINI CLIENT 
# ============================================================ 
 
def get_gemini_client(): 
    """ 
    Create Gemini AI client using GEMINI_API_KEY 
    from the .env file. 
    """ 
 
    api_key = os.getenv("GEMINI_API_KEY") 
 
    if not api_key: 
        raise Exception( 
            "Gemini API key not configured" 
        ) 
 
    return genai.Client( 
        api_key=api_key 
    ) 
 
 
# ============================================================ 
# HELPER FUNCTIONS 
# ============================================================ 
 
def get_employee_average_performance( 
    db: Session, 
    employee_id: int 
): 
    """ 
    Calculate the average performance rating for an employee. 
    """ 
 
    performances = ( 
        db.query(Performance) 
        .filter( 
            Performance.employee_id == employee_id 
        ) 
        .all() 
    ) 
 
    if not performances: 
        return 0 
 
    ratings = [] 
 
    for performance in performances: 
 
        rating = getattr( 
            performance, 
            "rating", 
            0 
        ) 
 
        if rating is not None: 
            ratings.append( 
                float(rating) 
            ) 
 
    if not ratings: 
        return 0 
 
    return round( 
        sum(ratings) / len(ratings), 
        2 
    ) 
 
 
def get_employee_task_count( 
    db: Session, 
    employee_id: int 
): 
    """ 
    Count tasks assigned to an employee. 
    """ 
 
    return ( 
        db.query(Task) 
        .filter( 
            Task.employee_id == employee_id 
        ) 
        .count() 
    ) 
 
 
def get_employee_completed_tasks( 
    db: Session, 
    employee_id: int 
): 
    """ 
    Count completed tasks. 
    """ 
 
    return ( 
        db.query(Task) 
        .filter( 
            Task.employee_id == employee_id, 
            Task.status == "Completed" 
        ) 
        .count() 
    ) 
 
 
def calculate_risk_level( 
    task_count, 
    performance_score 
): 
    """ 
    Simple AI fallback risk calculation. 
    """ 
 
    if task_count >= 5: 
        return "High" 
 
    if ( 
        performance_score > 0 
        and performance_score < 3 
    ): 
        return "High" 
 
    if task_count >= 3: 
        return "Medium" 
 
    if ( 
        performance_score > 0 
        and performance_score < 4 
    ): 
        return "Medium" 
 
    return "Low" 
 
 
# ============================================================ 
# WORKFORCE ANALYSIS 
# ============================================================ 
 
def create_workforce_analysis( 
    db: Session 
): 
    """ 
    Generate workforce analysis without Gemini. 
 
    Used as fallback when Gemini is unavailable. 
    """ 
 
    employees = db.query(Employee).all() 
    tasks = db.query(Task).all() 
 
    total_employees = len(employees) 
    total_tasks = len(tasks) 
 
    employee_performance_data = [] 
    employee_workload_data = [] 
 
    high_risk_employees = [] 
    medium_risk_employees = [] 
 
    for employee in employees: 
 
        performance_score = ( 
            get_employee_average_performance( 
                db, 
                employee.id 
            ) 
        ) 
 
        task_count = ( 
            get_employee_task_count( 
                db, 
                employee.id 
            ) 
        ) 
 
        completed_tasks = ( 
            get_employee_completed_tasks( 
                db, 
                employee.id 
            ) 
        ) 
 
        risk = calculate_risk_level( 
            task_count, 
            performance_score 
        ) 
 
        employee_performance_data.append( 
            f"{employee.name} " 
            f"({employee.department}) " 
            f"has an average performance score " 
            f"of {performance_score}." 
        ) 
 
        employee_workload_data.append( 
            f"{employee.name} is assigned " 
            f"{task_count} task(s), " 
            f"with {completed_tasks} completed." 
        ) 
 
        if risk == "High": 
            high_risk_employees.append( 
                employee.name 
            ) 
 
        elif risk == "Medium": 
            medium_risk_employees.append( 
                employee.name 
            ) 
 
    # -------------------------------------------------------- 
    # WORKFORCE AVERAGE PERFORMANCE 
    # -------------------------------------------------------- 
 
    all_scores = [] 
 
    performances = ( 
        db.query(Performance).all() 
    ) 
 
    for performance in performances: 
 
        rating = getattr( 
            performance, 
            "rating", 
            0 
        ) 
 
        if rating is not None: 
            all_scores.append( 
                float(rating) 
            ) 
 
    average_performance = 0 
 
    if all_scores: 
 
        average_performance = round( 
            sum(all_scores) / len(all_scores), 
            2 
        ) 
 
    # -------------------------------------------------------- 
    # ORGANIZATION RISK 
    # -------------------------------------------------------- 
 
    if len(high_risk_employees) > 0: 
 
        organization_risk = "High" 
 
    elif len(medium_risk_employees) > 0: 
 
        organization_risk = "Medium" 
 
    else: 
 
        organization_risk = "Low" 
 
    # -------------------------------------------------------- 
    # RECOMMENDATIONS 
    # -------------------------------------------------------- 
 
    recommendations = [] 
 
    if total_employees == 0: 
 
        recommendations.append( 
            "Add employees to the workforce system." 
        ) 
 
    if total_tasks == 0: 
 
        recommendations.append( 
            "Create and assign tasks to employees." 
        ) 
 
    # Employees without tasks 
 
    employees_without_tasks = [] 
 
    for employee in employees: 
 
        task_count = ( 
            get_employee_task_count( 
                db, 
                employee.id 
            ) 
        ) 
 
        if task_count == 0: 
 
            employees_without_tasks.append( 
                employee.name 
            ) 
 
    if employees_without_tasks: 
 
        recommendations.append( 
            "Assign tasks to employees with no " 
            "current workload: " 
            + ", ".join( 
                employees_without_tasks 
            ) 
            + "." 
        ) 
 
    # High risk recommendations 
 
    if high_risk_employees: 
 
        recommendations.append( 
            "Review workload and performance " 
            "for high-risk employees: " 
            + ", ".join( 
                high_risk_employees 
            ) 
            + "." 
        ) 
 
    # Performance recommendations 
 
    if average_performance == 0: 
 
        recommendations.append( 
            "Add employee performance ratings " 
            "to improve AI analysis accuracy." 
        ) 
 
    elif average_performance < 3: 
 
        recommendations.append( 
            "Provide additional training " 
            "and performance support." 
        ) 
 
    elif average_performance < 4: 
 
        recommendations.append( 
            "Monitor employee performance " 
            "and provide improvement guidance." 
        ) 
 
    else: 
 
        recommendations.append( 
            "Maintain the current performance level " 
            "and recognize high-performing employees." 
        ) 
 
    if not recommendations: 
 
        recommendations.append( 
            "The workforce appears balanced. " 
            "Continue monitoring performance " 
            "and workload." 
        ) 
 
    # -------------------------------------------------------- 
    # RESPONSE 
    # -------------------------------------------------------- 
 
    summary = ( 
        f"The workforce currently has an average " 
        f"performance score of {average_performance} " 
        f"across {total_employees} active employee(s) " 
        f"with {total_tasks} total task(s) assigned." 
    ) 
 
    if employee_performance_data: 
 
        performance_analysis = " ".join( 
            employee_performance_data 
        ) 
 
    else: 
 
        performance_analysis = ( 
            "No employee performance data " 
            "is currently available." 
        ) 
 
    if employee_workload_data: 
 
        workload_analysis = " ".join( 
            employee_workload_data 
        ) 
 
    else: 
 
        workload_analysis = ( 
            "No task data is currently available." 
        ) 
 
    return { 
        "summary": summary, 
        "performance_analysis": performance_analysis, 
        "workload_analysis": workload_analysis, 
        "risk_level": organization_risk, 
        "recommendations": recommendations, 
    } 
 
 
# ============================================================ 
# AI ASSISTANT 
# ============================================================ 
 
@router.get("/assistant") 
def ai_assistant( 
    question: str, 
    db: Session = Depends(get_db) 
): 
    """ 
    AI Workforce Assistant. 
 
    Uses Gemini AI to answer the user's question 
    based on real workforce database information. 
 
    If Gemini is unavailable, fallback analysis is returned. 
    """ 
 
    try: 
 
        # ---------------------------------------------------- 
        # GET WORKFORCE DATA 
        # ---------------------------------------------------- 
 
        fallback_answer = ( 
            create_workforce_analysis(db) 
        ) 
 
        # ---------------------------------------------------- 
        # GEMINI 
        # ---------------------------------------------------- 
 
        try: 
 
            client = get_gemini_client() 
 
            prompt = f""" 
You are an AI Workforce Assistant inside an 
Employee Workforce Management Platform. 
 
Your job is to answer the user's question 
accurately using the workforce data provided below. 
 
IMPORTANT RULES: 
 
1. Answer the user's EXACT question. 
2. Do NOT always return the entire workforce analysis. 
3. If the user asks about a specific employee, 
   focus mainly on that employee. 
4. If the user asks about performance, 
   explain performance. 
5. If the user asks about workload, 
   explain workload. 
6. If the user asks about tasks, 
   explain task information. 
7. If the user asks about risk, 
   explain risk. 
8. If the user asks for recommendations, 
   provide practical recommendations. 
9. If the user asks a general workforce question, 
   provide a general workforce answer. 
10. Use only the provided workforce data. 
11. Do not invent employee names, tasks, ratings, 
    or other information. 
12. Keep the answer professional and easy to understand. 
 
USER QUESTION: 
{question} 
 
WORKFORCE DATA: 
 
SUMMARY: 
{fallback_answer["summary"]} 
 
PERFORMANCE: 
{fallback_answer["performance_analysis"]} 
 
WORKLOAD: 
{fallback_answer["workload_analysis"]} 
 
RISK LEVEL: 
{fallback_answer["risk_level"]} 
 
RECOMMENDATIONS: 
{", ".join(fallback_answer["recommendations"])} 
 
Now answer the user's question directly. 
""" 
 
            response = client.models.generate_content( 
                model="gemini-3.6-flash", 
                contents=prompt 
            ) 
 
            gemini_answer = response.text 
 
            if not gemini_answer: 
 
                raise Exception( 
                    "Gemini returned an empty response" 
                ) 
 
            return { 
                "question": question, 
                "answer": { 
                    "summary": gemini_answer, 
                    "performance_analysis": 
                        fallback_answer[ 
                            "performance_analysis" 
                        ], 
                    "workload_analysis": 
                        fallback_answer[ 
                            "workload_analysis" 
                        ], 
                    "risk_level": 
                        fallback_answer[ 
                            "risk_level" 
                        ], 
                    "recommendations": 
                        fallback_answer[ 
                            "recommendations" 
                        ], 
                    "ai_source": "Gemini AI", 
                } 
            } 
 
        except Exception as gemini_error: 
 
            print( 
                "Gemini unavailable. " 
                "Using fallback AI:", 
                gemini_error 
            ) 
 
            fallback_answer["ai_source"] = ( 
                "Workforce Intelligence Engine" 
            ) 
 
            return { 
                "question": question, 
                "answer": fallback_answer 
            } 
 
    except Exception as error: 
 
        print( 
            "AI Assistant Error:", 
            error 
        ) 
 
        raise HTTPException( 
            status_code=500, 
            detail=str(error) 
        ) 
 
 
# ============================================================ 
# WORKFORCE INSIGHTS 
# ============================================================ 
 
@router.get("/workforce-insights") 
def workforce_insights( 
    db: Session = Depends(get_db) 
): 
 
    analysis = ( 
        create_workforce_analysis(db) 
    ) 
 
    return { 
        "workforce_insights": analysis 
    } 
 
 
# ============================================================ 
# GEMINI WORKFORCE INSIGHTS 
# ============================================================ 
 
@router.get("/gemini-workforce-insights") 
def gemini_workforce_insights( 
    db: Session = Depends(get_db) 
): 
 
    fallback_analysis = ( 
        create_workforce_analysis(db) 
    ) 
 
    try: 
 
        client = get_gemini_client() 
 
        prompt = f""" 
Analyze the following employee workforce data. 
 
Provide useful management insights including: 
 
- Overall workforce performance 
- Employee performance 
- Workload 
- Potential risks 
- Recommendations 
 
Workforce Data: 
 
{fallback_analysis} 
 
Give a professional and concise management analysis. 
""" 
 
        response = client.models.generate_content( 
            model="gemini-3.6-flash", 
            contents=prompt 
        ) 
 
        return { 
            "source": "Gemini AI", 
            "insights": response.text 
        } 
 
    except Exception as error: 
 
        return { 
            "source": 
                "Fallback Workforce Intelligence", 
            "message": 
                "Gemini is temporarily unavailable.", 
            "insights": 
                fallback_analysis, 
            "gemini_error": 
                str(error) 
        } 
 
 
# ============================================================ 
# EMPLOYEE ANALYSIS 
# ============================================================ 
 
@router.get("/employee-analysis/{employee_id}") 
def employee_analysis( 
    employee_id: int, 
    db: Session = Depends(get_db) 
): 
 
    employee = ( 
        db.query(Employee) 
        .filter( 
            Employee.id == employee_id 
        ) 
        .first() 
    ) 
 
    if not employee: 
 
        raise HTTPException( 
            status_code=404, 
            detail="Employee not found" 
        ) 
 
    performance_score = ( 
        get_employee_average_performance( 
            db, 
            employee.id 
        ) 
    ) 
 
    task_count = ( 
        get_employee_task_count( 
            db, 
            employee.id 
        ) 
    ) 
 
    completed_tasks = ( 
        get_employee_completed_tasks( 
            db, 
            employee.id 
        ) 
    ) 
 
    risk = calculate_risk_level( 
        task_count, 
        performance_score 
    ) 
 
    recommendations = [] 
 
    if task_count == 0: 
 
        recommendations.append( 
            "Assign suitable tasks " 
            "to this employee." 
        ) 
 
    if task_count >= 5: 
 
        recommendations.append( 
            "Review workload to prevent " 
            "employee overload." 
        ) 
 
    if performance_score == 0: 
 
        recommendations.append( 
            "Add performance ratings " 
            "for better analysis." 
        ) 
 
    elif performance_score < 3: 
 
        recommendations.append( 
            "Provide additional training " 
            "and support." 
        ) 
 
    else: 
 
        recommendations.append( 
            "Continue monitoring performance " 
            "and workload." 
        ) 
 
    return { 
        "employee": { 
            "id": employee.id, 
            "name": employee.name, 
            "role": employee.role, 
            "department": employee.department, 
        }, 
        "performance_score": 
            performance_score, 
        "assigned_tasks": 
            task_count, 
        "completed_tasks": 
            completed_tasks, 
        "risk_level": 
            risk, 
        "recommendations": 
            recommendations, 
    } 
 
 
# ============================================================ 
# PERFORMANCE ANALYSIS 
# ============================================================ 
 
@router.get("/performance-analysis/{rating}") 
def performance_analysis( 
    rating: float 
): 
 
    if rating >= 4: 
 
        analysis = ( 
            "Excellent performance. " 
            "Continue maintaining current productivity." 
        ) 
 
        recommendation = ( 
            "Recognize achievements and consider " 
            "additional responsibilities." 
        ) 
 
    elif rating >= 3: 
 
        analysis = ( 
            "Good performance with opportunities " 
            "for improvement." 
        ) 
 
        recommendation = ( 
            "Provide guidance to improve " 
            "performance further." 
        ) 
 
    elif rating >= 2: 
 
        analysis = ( 
            "Average performance that " 
            "requires attention." 
        ) 
 
        recommendation = ( 
            "Provide training and regular " 
            "performance feedback." 
        ) 
 
    else: 
 
        analysis = ( 
            "Low performance detected." 
        ) 
 
        recommendation = ( 
            "Create a performance improvement plan." 
        ) 
 
    return { 
        "rating": rating, 
        "analysis": analysis, 
        "recommendation": recommendation, 
    } 
 
 
# ============================================================ 
# TASK RECOMMENDATION 
# ============================================================ 
 
@router.get("/task-recommendation") 
def task_recommendation( 
    db: Session = Depends(get_db) 
): 
 
    employees = ( 
        db.query(Employee).all() 
    ) 
 
    recommendations = [] 
 
    for employee in employees: 
 
        task_count = ( 
            get_employee_task_count( 
                db, 
                employee.id 
            ) 
        ) 
 
        performance_score = ( 
            get_employee_average_performance( 
                db, 
                employee.id 
            ) 
        ) 
 
        if task_count == 0: 
 
            recommendation = ( 
                f"{employee.name} currently has " 
                f"no assigned tasks. " 
                f"Consider assigning new work." 
            ) 
 
        elif task_count >= 5: 
 
            recommendation = ( 
                f"{employee.name} has a high workload " 
                f"with {task_count} tasks. " 
                f"Avoid assigning additional tasks." 
            ) 
 
        else: 
 
            recommendation = ( 
                f"{employee.name} has a manageable " 
                f"workload and can be considered " 
                f"for suitable tasks." 
            ) 
 
        recommendations.append({ 
            "employee_id": 
                employee.id, 
            "employee_name": 
                employee.name, 
            "department": 
                employee.department, 
            "performance_score": 
                performance_score, 
            "assigned_tasks": 
                task_count, 
            "recommendation": 
                recommendation, 
        }) 
 
    return { 
        "task_recommendations": 
            recommendations 
    } 
 
 
# ============================================================
# SMART TASK ASSIGNMENT
# ============================================================

@router.post("/smart-task-assignment")
def smart_task_assignment(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees available"
        )

    employee_analysis = []

    best_employee = None
    best_score = None

    for employee in employees:

        # Current workload
        task_count = get_employee_task_count(
            db,
            employee.id
        )

        # Average performance
        performance_score = get_employee_average_performance(
            db,
            employee.id
        )

        # Completed tasks
        completed_tasks = get_employee_completed_tasks(
            db,
            employee.id
        )

        # --------------------------------------------
        # SMART SCORE CALCULATION
        # --------------------------------------------

        # Lower workload is better
        workload_score = max(
            0,
            5 - task_count
        )

        # Higher performance is better
        performance_component = performance_score

        # More completed tasks is better
        completed_score = min(
            completed_tasks,
            5
        )

        smart_score = (
            (workload_score * 0.5)
            + (performance_component * 0.3)
            + (completed_score * 0.2)
        )

        smart_score = round(
            smart_score,
            2
        )

        # --------------------------------------------
        # STORE EVERY EMPLOYEE
        # --------------------------------------------

        employee_analysis.append({
            "id": employee.id,
            "name": employee.name,
            "role": employee.role,
            "department": employee.department,
            "current_workload": task_count,
            "performance_score": performance_score,
            "completed_tasks": completed_tasks,
            "smart_score": smart_score
        })

        # --------------------------------------------
        # FIND BEST EMPLOYEE
        # --------------------------------------------

        if (
            best_score is None
            or smart_score > best_score
        ):

            best_score = smart_score
            best_employee = employee

    # --------------------------------------------
    # SORT EMPLOYEES BY SMART SCORE
    # --------------------------------------------

    employee_analysis.sort(
        key=lambda employee: employee["smart_score"],
        reverse=True
    )

    # --------------------------------------------
    # RESPONSE
    # --------------------------------------------

    return {
        "recommended_employee": {
            "id": best_employee.id,
            "name": best_employee.name,
            "role": best_employee.role,
            "department": best_employee.department
        },

        "current_workload": get_employee_task_count(
            db,
            best_employee.id
        ),

        "performance_score": get_employee_average_performance(
            db,
            best_employee.id
        ),

        "completed_tasks": get_employee_completed_tasks(
            db,
            best_employee.id
        ),

        "smart_score": best_score,

        "all_employees": employee_analysis,

        "reason": (
            "This employee is recommended using a balanced "
            "analysis of workload, performance and completed tasks."
        )
    }
 
# ============================================================ 
# EMPLOYEE RISK PREDICTION 
# ============================================================ 
 
@router.get("/employee-risk-prediction") 
def employee_risk_prediction( 
    db: Session = Depends(get_db) 
): 
 
    employees = ( 
        db.query(Employee).all() 
    ) 
 
    predictions = [] 
 
    for employee in employees: 
 
        performance_score = ( 
            get_employee_average_performance( 
                db, 
                employee.id 
            ) 
        ) 
 
        task_count = ( 
            get_employee_task_count( 
                db, 
                employee.id 
            ) 
        ) 
 
        completed_tasks = ( 
            get_employee_completed_tasks( 
                db, 
                employee.id 
            ) 
        ) 
 
        risk_level = ( 
            calculate_risk_level( 
                task_count, 
                performance_score 
            ) 
        ) 
 
        reasons = [] 
 
        if task_count >= 5: 
 
            reasons.append( 
                "High workload detected" 
            ) 
 
        if ( 
            performance_score > 0 
            and performance_score < 3 
        ): 
 
            reasons.append( 
                "Low performance rating" 
            ) 
 
        if task_count == 0: 
 
            reasons.append( 
                "No tasks currently assigned" 
            ) 
 
        if performance_score == 0: 
 
            reasons.append( 
                "No performance data available" 
            ) 
 
        if not reasons: 
 
            reasons.append( 
                "Workload and performance " 
                "appear stable" 
            ) 
 
        predictions.append({ 
            "employee_id": 
                employee.id, 
            "employee_name": 
                employee.name, 
            "department": 
                employee.department, 
            "performance_score": 
                performance_score, 
            "assigned_tasks": 
                task_count, 
            "completed_tasks": 
                completed_tasks, 
            "risk_level": 
                risk_level, 
            "risk_factors": 
                reasons, 
        }) 
 
    return { 
        "employee_risk_predictions": 
            predictions 
    } 