from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

# Import all models so SQLAlchemy registers all tables
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance

from app.routes.employee_routes import router as employee_router
from app.routes.task_routes import router as task_router
from app.routes.performance_routes import router as performance_router
from app.routes.ai_routes import router as ai_router


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AI Employee Workforce Platform",
    description="AI-powered Employee Workforce Management Platform",
    version="1.0.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://ai-employee-workforce-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


# ==========================================
# INCLUDE ROUTES
# ==========================================

app.include_router(employee_router)
app.include_router(task_router)
app.include_router(performance_router)
app.include_router(ai_router)


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AI Employee Workforce Platform API is running successfully 🚀",
        "status": "success"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }