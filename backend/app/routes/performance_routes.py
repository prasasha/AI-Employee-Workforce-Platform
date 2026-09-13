from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.performance import Performance
from app.models.employee import Employee
from app.schemas.performance import PerformanceCreate, PerformanceUpdate, PerformanceResponse

router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PerformanceResponse)
def create_performance(
    performance: PerformanceCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == performance.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found. Cannot add performance record."
        )

    new_performance = Performance(
        rating=performance.rating,
        review=performance.review,
        period=performance.period,
        employee_id=performance.employee_id
    )

    db.add(new_performance)
    db.commit()
    db.refresh(new_performance)

    return new_performance


@router.get("/", response_model=list[PerformanceResponse])
def get_all_performance(
    db: Session = Depends(get_db)
):
    return db.query(Performance).all()


@router.get("/{performance_id}", response_model=PerformanceResponse)
def get_performance_by_id(
    performance_id: int,
    db: Session = Depends(get_db)
):
    performance = db.query(Performance).filter(
        Performance.id == performance_id
    ).first()

    if performance is None:
        raise HTTPException(status_code=404, detail="Performance record not found")

    return performance


@router.put("/{performance_id}", response_model=PerformanceResponse)
def update_performance(
    performance_id: int,
    performance: PerformanceUpdate,
    db: Session = Depends(get_db)
):
    existing = db.query(Performance).filter(
        Performance.id == performance_id
    ).first()

    if existing is None:
        raise HTTPException(status_code=404, detail="Performance record not found")

    update_data = performance.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{performance_id}")
def delete_performance(
    performance_id: int,
    db: Session = Depends(get_db)
):
    performance = db.query(Performance).filter(
        Performance.id == performance_id
    ).first()

    if performance is None:
        raise HTTPException(status_code=404, detail="Performance record not found")

    db.delete(performance)
    db.commit()

    return {"message": "Performance record deleted successfully"}