"""lead and salesperson tables

Revision ID: 1ac052d05d7b
Revises: 
Create Date: 2024-11-19 02:37:33.704247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1ac052d05d7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('salespersons',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('leads',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('source', sa.Enum('REFERRAL', 'WEBSITE', 'COLD_CALL', 'EVENT', name='leadsource'), nullable=False),
    sa.Column('interest_level', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='leadinterestlevel'), nullable=False),
    sa.Column('status', sa.Enum('NEW', 'CLOSED', 'QUALIFIED', 'CONTACTED', name='leadstatus'), nullable=False),
    sa.Column('assigned_salesperson', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['assigned_salesperson'], ['salespersons.name'], ),
    sa.PrimaryKeyConstraint('id', 'lead_id'),
    sa.UniqueConstraint('lead_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leads')
    op.drop_table('salespersons')
    # ### end Alembic commands ###
