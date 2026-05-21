"""fix_category_fk_restrict

Revision ID: 859f0505122e
Revises: ea964a2558f2
Create Date: 2026-05-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = '859f0505122e'
down_revision: Union[str, Sequence[str], None] = 'ea964a2558f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('blog_post_category_id_fkey', 'blog_post', type_='foreignkey')
    op.create_foreign_key(
        'blog_post_category_id_fkey',
        'blog_post',
        'blog_category',
        ['category_id'],
        ['id'],
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    op.drop_constraint('blog_post_category_id_fkey', 'blog_post', type_='foreignkey')
    op.create_foreign_key(
        'blog_post_category_id_fkey',
        'blog_post',
        'blog_category',
        ['category_id'],
        ['id']
    )