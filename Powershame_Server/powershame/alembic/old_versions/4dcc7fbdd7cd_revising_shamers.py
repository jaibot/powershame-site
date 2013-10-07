"""revising shamers

Revision ID: 4dcc7fbdd7cd
Revises: 34875d9eb3e6
Create Date: 2013-07-30 12:35:36.743812

"""

# revision identifiers, used by Alembic.
revision = '4dcc7fbdd7cd'
down_revision = '34875d9eb3e6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('shamers')
    op.add_column('user', sa.Column( 'is_registered', sa.Boolean, default=True ) )
    op.create_table(
        'contact_info',
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'contact_type', sa.SmallInteger ),
        sa.Column( 'identifier', sa.String(512) )
    )
    op.create_table(
        'shamers',
        sa.Column( 'user', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'shamer', sa.Integer, sa.ForeignKey( 'user.id' ) )
    )

def downgrade():
    op.drop_table('shamers')
    op.drop_table('contact_info')
    op.drop_column( 'user','is_registered' )
    op.create_table(
        'shamers',
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'shamer', sa.String(256) )
    )
