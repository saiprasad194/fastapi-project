"""user role table

Revision ID: e4b03741615b
Revises: f5c564c89a80
Create Date: 2024-05-18 16:21:21.928203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e4b03741615b'
down_revision: Union[str, None] = 'f5c564c89a80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'deleted')
    op.drop_column('department', 'deleted')
    op.drop_column('location', 'deleted')
    op.drop_column('roles', 'deleted')
    op.drop_column('subcategory', 'deleted')
    op.drop_column('user_role', 'deleted')
    op.drop_column('users', 'deleted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('user_role', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('subcategory', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('roles', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('location', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('department', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('category', sa.Column('deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
