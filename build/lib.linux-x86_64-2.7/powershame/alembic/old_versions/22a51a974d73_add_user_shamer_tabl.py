"""add user-shamer table

Revision ID: 22a51a974d73
Revises: 3c8f59db2f3
Create Date: 2013-08-07 20:48:14.920726

"""

# revision identifiers, used by Alembic.
revision = '22a51a974d73'
down_revision = '3c8f59db2f3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_shamers',
        sa.Column( 'user', sa.Integer, sa.ForeignKey('user.id'), index=True ),
        sa.Column( 'shamer', sa.Integer, sa.ForeignKey('contact_info.id') )
    )


def downgrade():
    op.drop_table( 'user_shamers' )
