from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.users.helpers import get_current_user
from app.helpers import get_db
from app.LDCS.models import Location, Department, Category, SubCategory
from app.LDCS.schemas import LocationSchema, DepartmentSchema, DepartmentOutSchema, ListDepartmentsSchema, \
    CategorySchema, CategoryOutSchema, SubcategorySchema, SubcategoryOutSchema
from fastapi import APIRouter
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException
from app.users.schemas import UserOut
from sqlalchemy.orm import subqueryload

router = APIRouter()

############################################ Location Routes ###############################################


@router.post("/location")
async def add_location(location: LocationSchema,
                       user: UserOut = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    location_model = Location(**location.dict())
    db.add(location_model)
    db.commit()
    return {"response": "Location Added Successfully"}


@router.get("/location/{location_id}")
async def get_location(location_id,
                       user: UserOut = Depends(get_current_user),
                       db: Session = Depends(get_db)
                       ):
    try:
        location = db.query(Location).filter(Location.id == location_id).one()
        return location
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Location not found")


@router.get("/locations")
async def get_locations(db: Session = Depends(get_db), user=Depends(get_current_user), ):
    locations = db.query(Location).all()
    return locations




############################################ Department Routes ###############################################

@router.post("/location/{location_id}/department", response_model=DepartmentOutSchema)
async def add_department_to_location(location_id,
                                     department_schema: DepartmentSchema,
                                     user: UserOut = Depends(get_current_user),
                                     db: Session = Depends(get_db)):
    try:
        location = db.query(Location).filter(Location.id == location_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Location not found")
    department_model = Department(location_id=location_id,
                                  department_name=department_schema.department_name
                                  )
    db.add(department_model)
    db.commit()
    departmentout = DepartmentOutSchema(location_id=location_id,
                                        location_name=location.location_name,
                                        department_id=department_model.id,
                                        department_name=department_model.department_name)
    return departmentout


@router.get("/location/{location_id}/departments")
async def get_departments_of_location(location_id, user: UserOut = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    try:
        location = db.query(Location).filter(Location.id == location_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Location not found")
    departments = db.query(Department).filter(Department.location_id == location_id).all()
    list_departments = []
    for department in departments:
        department_schema = DepartmentOutSchema(location_id=location.id, location_name=location.location_name,
                                                department_id=department.id, department_name=department.department_name
                                                )
        list_departments.append(department_schema)
    return list_departments



############################################ Category Routes ###############################################



@router.post("/location/{location_id}/department/{department_id}/category")
async def add_category_to_department(location_id, department_id, category_schema: CategorySchema,
                                     user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        department = (db.query(Department).
                      filter(Department.id == department_id, Department.location_id == location_id).
                      options(subqueryload(Department.location))
                      .one())
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Department not found")
    category_model = Category(department_id=department_id,
                              category_name=category_schema.category_name
                              )
    db.add(category_model)
    db.commit()
    category_out = CategoryOutSchema(category_id=category_model.id,
                                     category_name=category_model.category_name,
                                     location_id=location_id,
                                     location_name=department.location.location_name,
                                     department_id=department_id,
                                     department_name=department.department_name
                                     )
    return category_out


@router.get("/location/{location_id}/department/{department_id}/categories")
async def get_departments_of_location(location_id, department_id, user: UserOut = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    try:
        department = (db.query(Department).
                      filter(Department.id == department_id, Department.location_id == location_id).
                      options(subqueryload(Department.location))
                      .one())
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Department not found")
    categories = db.query(Category).filter(Category.department_id == department_id).all()
    list_categories = []
    for category in categories:
        category_schema = CategoryOutSchema(location_id=department.location.id,
                                            location_name=department.location.location_name,
                                            department_id=department.id, department_name=department.department_name,
                                            category_id=category.id,
                                            category_name=category.category_name
                                            )
        list_categories.append(category_schema)
    return list_categories




############################################ Subcategory Routes ###############################################



@router.post("/department/{department_id}/category/{category_id}/subcategory")
async def add_subcategory_to_category(department_id, category_id,
                                        subcategory_schema: SubcategorySchema,
                                        user: UserOut = Depends(get_current_user),
                                        db: Session = Depends(get_db)):
    try:
        category = (db.query(Category).
                      filter(Category.id == category_id, Category.department_id == department_id).
                      options(subqueryload(Category.department))
                      .one())
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Category not found")
    subcategory_model = SubCategory(category_id=category_id,
                              subcategory_name=subcategory_schema.subcategory_name
                              )
    db.add(subcategory_model)
    db.commit()
    subcategory_out = SubcategoryOutSchema(subcategory_id=subcategory_model.id,
                                     subcategory_name=subcategory_model.subcategory_name,
                                     department_id=department_id,
                                     department_name=category.department.department_name,
                                     category_id = category.id,
                                     category_name = category.category_name
                                     )
    return subcategory_out


@router.get("/department/{department_id}/category/{category_id}/subcategories")
async def get_subcategories_of_categgory(department_id,category_id, user: UserOut = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    try:
        category = (db.query(Category).
                      filter(Category.id == category_id, Category.department_id == department_id).
                      options(subqueryload(Category.department))
                      .one())
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Department not found")
    subcategories = db.query(SubCategory).filter(SubCategory.category_id == category_id).all()
    list_subcategories = []
    for subcategory in subcategories:
        subcategory_schema = SubcategoryOutSchema(
                            department_id=category.department.id,
                            department_name=category.department.department_name,
                            category_id=category.id,
                            category_name=category.category_name,
                            subcategory_id = subcategory.id,
                            subcategory_name = subcategory.subcategory_name
        )
        list_subcategories.append(subcategory_schema)
    return list_subcategories