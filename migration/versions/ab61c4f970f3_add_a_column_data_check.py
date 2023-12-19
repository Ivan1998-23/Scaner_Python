"""Add a column data_check

Revision ID: ab61c4f970f3
Revises: 614324afe9b9
Create Date: 2023-12-19 17:33:42.399487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab61c4f970f3'
down_revision: Union[str, None] = '614324afe9b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
