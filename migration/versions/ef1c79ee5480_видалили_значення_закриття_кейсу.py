"""видалили значення закриття кейсу

Revision ID: ef1c79ee5480
Revises: 261887bb05af
Create Date: 2023-12-21 15:10:16.795072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef1c79ee5480'
down_revision: Union[str, None] = '261887bb05af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'data_checked')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('data_checked', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
