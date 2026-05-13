"""increase_slug_length_to_255

Revision ID: 52fd0fcb69ae
Revises: bd9cb82a3c71
Create Date: 2026-05-13 14:04:54.200490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52fd0fcb69ae'
down_revision: Union[str, Sequence[str], None] = 'bd9cb82a3c71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
