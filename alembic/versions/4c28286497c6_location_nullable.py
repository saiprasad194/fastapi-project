"""location nullable

Revision ID: 4c28286497c6
Revises: ebadf5d85eb8
Create Date: 2024-05-18 16:27:35.175334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4c28286497c6'
down_revision: Union[str, None] = 'ebadf5d85eb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'category_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('category', 'department_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('department', 'department_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('department', 'location_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('location', 'location_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'location', ['location_name'])
    op.alter_column('subcategory', 'category_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('subcategory', 'subcategory_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subcategory', 'subcategory_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('subcategory', 'category_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_constraint(None, 'location', type_='unique')
    op.alter_column('location', 'location_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('department', 'location_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('department', 'department_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('category', 'department_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('category', 'category_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
