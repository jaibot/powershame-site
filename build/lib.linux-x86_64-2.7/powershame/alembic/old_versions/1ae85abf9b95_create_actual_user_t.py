"""create actual user table

Revision ID: 1ae85abf9b95
Revises: 3c17ef18ad2d
Create Date: 2013-07-11 11:24:10.583905

"""

# revision identifiers, used by Alembic.
revision = '1ae85abf9b95'
down_revision = '3c17ef18ad2d'

from alembic import op
from alembic.op import *
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(32), nullable=False ),
        sa.Column('password', sa.String(64), nullable=False)
    )


def downgrade():
    op.drop_table('user')
    pass
