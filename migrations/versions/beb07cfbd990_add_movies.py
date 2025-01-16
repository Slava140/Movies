"""add movies

Revision ID: beb07cfbd990
Revises: 
Create Date: 2025-01-15 17:15:57.486923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beb07cfbd990'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('show_id', sa.String(length=30), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('director', sa.String(length=500), nullable=False),
    sa.Column('cast', sa.String(length=500), nullable=False),
    sa.Column('country', sa.String(length=500), nullable=False),
    sa.Column('date_added', sa.Date(), nullable=False),
    sa.Column('release_year', sa.Integer(), nullable=False),
    sa.Column('rating', sa.String(length=30), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('listed_in', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    # ### end Alembic commands ###
