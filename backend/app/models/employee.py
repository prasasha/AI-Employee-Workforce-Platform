from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String)
    status = Column(String, default="Active")

    tasks = relationship("Task", back_populates="employee")
    performance_records = relationship("Performance", back_populates="employee")