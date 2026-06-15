"""initial_tables

Revision ID: 3d1b492c2504
Revises: 
Create Date: 2026-06-14 20:48:59.808609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d1b492c2504'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS menu")

def downgrade():
    op.execute("DROP SCHEMA IF EXISTS menu CASCADE")
