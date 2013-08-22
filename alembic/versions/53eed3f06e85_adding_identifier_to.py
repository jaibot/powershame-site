"""adding identifier to sessions

Revision ID: 53eed3f06e85
Revises: d08e7d4e5ca
Create Date: 2013-07-18 11:13:37.789636

"""

# revision identifiers, used by Alembic.
revision = '53eed3f06e85'
down_revision = 'd08e7d4e5ca'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('session')
    op.create_table(
        'session',
        sa.Column( 'id',sa.String(256), primary_key=True ),
        sa.Column( 'prefix',sa.String(256) ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime )
    )


def downgrade():
    op.drop_table(table_name='session')
    op.create_table(
        'session',
        sa.Column( 'prefix',sa.String(256), primary_key=True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'start_time', sa.DateTime )
    )

