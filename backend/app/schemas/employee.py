from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    role: str
    department: str


class EmployeeUpdate(BaseModel):
    name: str
    role: str
    department: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    department: str
    status: str

    class Config:
        from_attributes = True