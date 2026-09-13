from pydantic import BaseModel
from typing import Optional

class PerformanceCreate(BaseModel):
    rating: float
    review: Optional[str] = None
    period: str
    employee_id: int

class PerformanceUpdate(BaseModel):
    rating: Optional[float] = None
    review: Optional[str] = None
    period: Optional[str] = None
    employee_id: Optional[int] = None

class PerformanceResponse(BaseModel):
    id: int
    rating: float
    review: Optional[str] = None
    period: str
    employee_id: int

    class Config:
        from_attributes = True