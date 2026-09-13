from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance


def seed_database():
    db: Session = SessionLocal()

    try:
        # Only seed when database is empty
        if db.query(Employee).count() > 0:
            return

        # Employees
        mathiyas = Employee(
            name="Mathiyas",
            role="Full Stack Developer",
            department="IT",
            status="Active"
        )

        prasanth = Employee(
            name="Prasanth",
            role="Data Engineer",
            department="CSE",
            status="Active"
        )

        yuva = Employee(
            name="Yuva",
            role="AI Engineer",
            department="IT",
            status="Active"
        )

        db.add_all([mathiyas, prasanth, yuva])
        db.commit()

        db.refresh(mathiyas)
        db.refresh(prasanth)
        db.refresh(yuva)

        # Tasks
        tasks = [
            Task(
                title="Setup database schema",
                description="Design and implement initial DB schema",
                status="pending",
                priority="high",
                employee_id=mathiyas.id
            ),
            Task(
                title="Monitor Priyam",
                description="24/7 chating",
                status="In Progress",
                priority="High",
                employee_id=mathiyas.id
            ),
            Task(
                title="Fix login page bug",
                description="User login la validation error irukku",
                status="In Progress",
                priority="High",
                employee_id=yuva.id
            )
        ]

        db.add_all(tasks)

        # Performance
        performance_records = [
            Performance(
                rating=4.5,
                review="Excellent performance and good task contribution",
                period="September 2026",
                employee_id=mathiyas.id
            ),
            Performance(
                rating=4.0,
                review="Good performance. Completed assigned tasks effectively and showed good technical skills.",
                period="September 2026",
                employee_id=mathiyas.id
            ),
            Performance(
                rating=4.5,
                review="Good performance and completed tasks on time",
                period="September 2026",
                employee_id=prasanth.id
            ),
            Performance(
                rating=3.0,
                review="Good performance, completed tasks on time",
                period="Q3 2026",
                employee_id=yuva.id
            )
        ]

        db.add_all(performance_records)
        db.commit()

        print("Demo database seeded successfully.")

    finally:
        db.close()
