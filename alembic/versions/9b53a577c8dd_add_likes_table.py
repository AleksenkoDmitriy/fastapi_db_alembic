"""add_likes_table

Revision ID: 9b53a577c8dd
Revises: 859f0505122e
Create Date: 2026-05-21 19:17:52.768809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b53a577c8dd'
down_revision: Union[str, Sequence[str], None] = '859f0505122e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('blog_like',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['blog_post.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['auth_user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('post_id', 'user_id', name='unique_post_user_like')
    )
    op.create_index('ix_blog_like_id', 'blog_like', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index('ix_blog_like_id', table_name='blog_like')
    op.drop_table('blog_like')