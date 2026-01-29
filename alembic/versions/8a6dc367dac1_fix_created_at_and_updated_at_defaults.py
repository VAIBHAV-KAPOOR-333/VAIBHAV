"""fix created_at and updated_at defaults

Revision ID: 8a6dc367dac1
Revises: ae618d227018
Create Date: 2026-01-16 12:15:01.936411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "8a6d367dac1"
down_revision = "ae618d227018"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    op.alter_column(
        "users",
        "updated_at",
        existing_type=sa.DateTime(),
        server_default=sa.text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "users",
        "updated_at",
        server_default=None,
        existing_type=sa.DateTime(),
    )

    op.alter_column(
        "users",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(),
    )