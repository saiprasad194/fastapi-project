from pydantic import BaseModel, Field


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserSignup(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)


# Define an Enum for roles


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
