"""new session format

Revision ID: 341a2731aaea
Revises: 53eed3f06e85
Create Date: 2013-07-23 16:30:53.620437

"""

# revision identifiers, used by Alembic.
revision = '341a2731aaea'
down_revision = '53eed3f06e85'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'session',
        sa.Column( 'prefix', sa.String(256), primary_key = True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime ),
        sa.Column( 'end_time', sa.DateTime )
    )


def downgrade():
    op.drop_table('session')
    op.create_table(
        'session',
        sa.Column( 'id',sa.String(256), primary_key=True ),
        sa.Column( 'prefix',sa.String(256) ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime )
    )
    pass
