"""adding shamers

Revision ID: 34875d9eb3e6
Revises: 341a2731aaea
Create Date: 2013-07-26 03:42:08.092873

"""

# revision identifiers, used by Alembic.
revision = '34875d9eb3e6'
down_revision = '341a2731aaea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'shamers',
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'shamer', sa.String(256) )
    )


def downgrade():
    op.drop_table('shamers')
