"""видалив дефаулт в часі

Revision ID: 56ae21a75a57
Revises: 9f08dad0790c
Create Date: 2024-01-05 17:40:20.149599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56ae21a75a57'
down_revision: Union[str, None] = '9f08dad0790c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
