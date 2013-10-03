"""new session format

Revision ID: 108644ea05a8
Revises: 5291636049dd
Create Date: 2013-08-05 10:42:05.289112

"""

# revision identifiers, used by Alembic.
revision = '108644ea05a8'
down_revision = '5291636049dd'

from alembic.op import Operations as op #autocomplete fix hack
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'session',
        sa.Column( 'id', sa.Integer, primary_key=True ),
        sa.Column( 'user', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'source', sa.Integer, sa.ForeignKey( 'client.id' ) ),
        sa.Column( 'name', sa.String(256) ),
        sa.Column( 'start_time', sa.DateTime ),
        sa.Column( 'end_time', sa.DateTime )
    )

def downgrade():
    op.drop_table( 'session' )
    op.create_table(
        'session',
        sa.Column( 'prefix', sa.String(256), primary_key = True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime ),
        sa.Column( 'end_time', sa.DateTime )
    )
    op.drop_table( 'client' )
    op.create_table(
        'token',
        sa.Column( 'id', sa.String(256), primary_key=True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey('user.id') )
    )
