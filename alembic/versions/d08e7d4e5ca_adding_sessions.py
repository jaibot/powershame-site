"""adding sessions

Revision ID: d08e7d4e5ca
Revises: 1df178ecd458
Create Date: 2013-07-16 16:52:47.213799

"""

# revision identifiers, used by Alembic.
revision = 'd08e7d4e5ca'
down_revision = '1df178ecd458'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'session',
        sa.Column( 'prefix',sa.String(256), primary_key=True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime )
    )


def downgrade():
    op.drop_table( 'session' )
