from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship


class Location(BaseModel):
    __tablename__ = "location"
    location_name = Column(String(255),unique=True,nullable=False)

    department = relationship("Department", back_populates="location")


class Department(BaseModel):
    __tablename__ = "department"

    department_name = Column(String(255),nullable=False)
    location_id = Column(Integer,ForeignKey("location.id"),nullable=False)

    location = relationship("Location",back_populates="department")
    category = relationship("Category",back_populates="department")


class Category(BaseModel):
    __tablename__ = "category"

    category_name = Column(String(255),nullable=False)
    department_id = Column(Integer,ForeignKey("department.id"),nullable=False)
    department = relationship("Department", back_populates="category")
    subcategories = relationship("SubCategory", back_populates="category")


class SubCategory(BaseModel):
    __tablename__ = "subcategory"

    category_id = Column(Integer, ForeignKey("category.id"),nullable=False)
    subcategory_name = Column(String(255),nullable=False)
    category = relationship("Category", back_populates="subcategories")



