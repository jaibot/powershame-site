"""adding token object

Revision ID: 1df178ecd458
Revises: 36f506e16686
Create Date: 2013-07-13 01:22:23.863068

"""

# revision identifiers, used by Alembic.
revision = '1df178ecd458'
down_revision = '36f506e16686'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'token',
        sa.Column( 'id',sa.String(256), primary_key=True ),
        sa.Column( 'user_id', sa.Integer )
    )


def downgrade():
    op.drop_table( 'token' )
