"""create first commit

Revision ID: 614324afe9b9
Revises: 
Create Date: 2023-12-19 17:32:17.353864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '614324afe9b9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'data_checked')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('data_checked', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
