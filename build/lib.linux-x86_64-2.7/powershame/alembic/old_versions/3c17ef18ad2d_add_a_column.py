"""add a column

Revision ID: 3c17ef18ad2d
Revises: fde787ea41b
Create Date: 2013-07-11 11:17:25.749889

"""

# revision identifiers, used by Alembic.
revision = '3c17ef18ad2d'
down_revision = 'fde787ea41b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account', sa.Column('coolness', sa.Integer))
    pass


def downgrade():
    pass
