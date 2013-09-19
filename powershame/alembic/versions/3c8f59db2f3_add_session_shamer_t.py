"""add session-shamer table

Revision ID: 3c8f59db2f3
Revises: 220b262e2716
Create Date: 2013-08-07 14:25:33.460003

"""

# revision identifiers, used by Alembic.
revision = '3c8f59db2f3'
down_revision = '220b262e2716'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'session_shamers',
        sa.Column( 'session', sa.Integer, sa.ForeignKey('session.id') ),
        sa.Column( 'shamer', sa.Integer, sa.ForeignKey('contact_info.id') )
    )


def downgrade():
    op.drop_table( 'session_shamers' )
