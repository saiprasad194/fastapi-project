from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from app.db.database import engine, Base
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
from enum import Enum as Enumc
from app.models import BaseModel


class RolesEnum(str, Enumc):
    admin = "admin"
    user = "user"

#
# user_roles_association = Table(
#     'user_roles_association',
#     BaseModel,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('role_id', Integer, ForeignKey('roles.id'))
# )


class UserRole(BaseModel):
    __tablename__ = 'user_role'

    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'),nullable=False)

    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    # roles = relationship("Role", secondary=user_roles_association, back_populates="users")
    user_roles = relationship('UserRole', back_populates='user')
    # roles = relationship('Role', secondary='user_role', back_populates='users', overlaps="user_roles")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bytes(bcrypt.gensalt()))

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode("utf-8"))


class Role(BaseModel):
    __tablename__ = "roles"

    role_name = Column(String(255), unique=True)

    user_roles = relationship('UserRole', back_populates='role')
    # users = relationship('User', secondary='user_role', back_populates='roles',overlaps="user_roles")
