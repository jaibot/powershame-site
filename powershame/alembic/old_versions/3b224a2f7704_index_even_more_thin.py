"""index even more things

Revision ID: 3b224a2f7704
Revises: 4b4b3a87ceb9
Create Date: 2013-08-08 12:07:44.466535

"""

# revision identifiers, used by Alembic.
revision = '3b224a2f7704'
down_revision = '4b4b3a87ceb9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index( 'ix_client_token','client', [ 'token' ] )


def downgrade():
    op.drop_index( 'ix_client_token','client', [ 'token' ] )
