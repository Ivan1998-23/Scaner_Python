"""додали дати перевірки та дзвінка

Revision ID: 365029bb7610
Revises: e9f234c39878
Create Date: 2024-01-04 13:33:05.023630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '365029bb7610'
down_revision: Union[str, None] = 'e9f234c39878'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('address', sa.Column('data_checked', sa.DateTime(), nullable=True))
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_column('address', 'data_checked')
    pass
    # ### end Alembic commands ###
