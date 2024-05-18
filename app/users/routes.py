from app.users.schemas import UserOut, UserSignup, TokenSchema, UserOut, TokenPayload
from app.users.helpers import create_access_token, create_refresh_token, get_current_user, validate_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.users.models import User, UserRole, Role
from app.helpers import get_db
from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserSignup, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    print("started executing query")
    user = db.query(User).filter(User.email == data.email).first()
    print("completed executing query")
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        "first_name": data.first_name,
        "last_name": data.last_name
    }
    user_object = User(**user)
    user_object.set_password(data.password)
    db.add(user_object)
    db.commit()
    user['id'] = user_object.id
    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    query = (
        db.query(Role)
        .join(UserRole)
        .join(User)
        .filter(User.id == user.id)
    )
    user_roles = query.all()
    role_ids = [role.id for role in user_roles]
    return {
        "access_token": create_access_token(user.email, role_ids),
        "refresh_token": create_refresh_token(user.email, role_ids),
    }
