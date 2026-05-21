"""fix_slug_length

Revision ID: ea964a2558f2
Revises: 52fd0fcb69ae
Create Date: 2026-05-18 07:03:33.124472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ea964a2558f2'
down_revision: Union[str, Sequence[str], None] = '52fd0fcb69ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('blog_category', 'slug', type_=sa.String(length=255))


def downgrade() -> None:
    op.alter_column('blog_category', 'slug', type_=sa.String(length=50))