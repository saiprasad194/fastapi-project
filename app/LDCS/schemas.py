from pydantic import BaseModel, Field
from typing import List


class LocationSchema(BaseModel):
    location_name: str


class DepartmentSchema(BaseModel):
    department_name: str

class DepartmentOutSchema(BaseModel):
    department_id: int
    department_name : str
    location_id: int
    location_name: str


class ListDepartmentsSchema(BaseModel):
    departments : List[DepartmentOutSchema]




class CategorySchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    category_id: int
    category_name: str
    department_id: int
    department_name : str
    location_id: int
    location_name: str


class SubcategorySchema(BaseModel):
    subcategory_name: str

class SubcategoryOutSchema(BaseModel):
    category_id: int
    category_name: str
    department_id: int
    department_name : str
    subcategory_id: int
    subcategory_name: str