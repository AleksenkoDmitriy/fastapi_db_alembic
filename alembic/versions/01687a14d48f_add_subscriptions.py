"""add_subscriptions

Revision ID: 01687a14d48f
Revises: 9b53a577c8dd
Create Date: 2026-05-22 10:45:03.703102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01687a14d48f'
down_revision: Union[str, Sequence[str], None] = '9b53a577c8dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS blog_subscription (
            id SERIAL PRIMARY KEY,
            follower_id INTEGER NOT NULL,
            following_id INTEGER NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                           WHERE constraint_name = 'blog_subscription_follower_id_fkey') THEN
                ALTER TABLE blog_subscription 
                ADD CONSTRAINT blog_subscription_follower_id_fkey 
                FOREIGN KEY (follower_id) REFERENCES auth_user(id) ON DELETE CASCADE;
            END IF;
        END
        $$;
    """)
    
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                           WHERE constraint_name = 'blog_subscription_following_id_fkey') THEN
                ALTER TABLE blog_subscription 
                ADD CONSTRAINT blog_subscription_following_id_fkey 
                FOREIGN KEY (following_id) REFERENCES auth_user(id) ON DELETE CASCADE;
            END IF;
        END
        $$;
    """)
    
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                           WHERE constraint_name = 'unique_follow') THEN
                ALTER TABLE blog_subscription 
                ADD CONSTRAINT unique_follow UNIQUE (follower_id, following_id);
            END IF;
        END
        $$;
    """)
    
    op.execute("CREATE INDEX IF NOT EXISTS ix_blog_subscription_id ON blog_subscription(id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_blog_subscription_follower_id ON blog_subscription(follower_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_blog_subscription_following_id ON blog_subscription(following_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_blog_subscription_following_id")
    op.execute("DROP INDEX IF EXISTS ix_blog_subscription_follower_id")
    op.execute("DROP INDEX IF EXISTS ix_blog_subscription_id")
    
    op.execute("ALTER TABLE blog_subscription DROP CONSTRAINT IF EXISTS unique_follow")
    op.execute("ALTER TABLE blog_subscription DROP CONSTRAINT IF EXISTS blog_subscription_following_id_fkey")
    op.execute("ALTER TABLE blog_subscription DROP CONSTRAINT IF EXISTS blog_subscription_follower_id_fkey")
    
    op.execute("DROP TABLE IF EXISTS blog_subscription")
