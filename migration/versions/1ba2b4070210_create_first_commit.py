"""create first commit

Revision ID: 1ba2b4070210
Revises: 
Create Date: 2023-12-19 15:45:58.342464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ba2b4070210'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('svmap')
    op.drop_table('logscan')
    op.drop_table('address')
    op.drop_table('nmap')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nmap',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('other', sa.VARCHAR(length=255), nullable=True),
    sa.Column('id_address', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id_address'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_address')
    )
    op.create_table('address',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ip', sa.VARCHAR(length=25), nullable=False),
    sa.Column('update', sa.DATETIME(), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=True),
    sa.Column('violation', sa.TEXT(), nullable=True),
    sa.Column('comments', sa.TEXT(), nullable=True),
    sa.Column('password', sa.TEXT(), nullable=True),
    sa.Column('checked', sa.BOOLEAN(), nullable=True),
    sa.Column('looked', sa.BOOLEAN(), nullable=True),
    sa.Column('status', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip')
    )
    op.create_table('logscan',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('start_time', sa.DATETIME(), nullable=True),
    sa.Column('ips', sa.VARCHAR(length=25), nullable=False),
    sa.Column('result', sa.BOOLEAN(), nullable=True),
    sa.Column('command', sa.VARCHAR(length=20), nullable=True),
    sa.Column('other', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('svmap',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ports', sa.VARCHAR(length=255), nullable=True),
    sa.Column('version', sa.VARCHAR(length=50), nullable=True),
    sa.Column('dev_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('id_address', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id_address'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_address')
    )
    # ### end Alembic commands ###
