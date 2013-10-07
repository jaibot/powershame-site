"""fixing shamer relationship

Revision ID: c4f2a3d329e
Revises: 4dcc7fbdd7cd
Create Date: 2013-07-31 14:55:35.181419

"""

# revision identifiers, used by Alembic.
revision = 'c4f2a3d329e'
down_revision = '4dcc7fbdd7cd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('contact_info')
    op.drop_table('shamers')
    op.create_table(
        'contact_info',
        sa.Column( 'id', sa.Integer, primary_key = True ),
        sa.Column( 'user_id', sa.Integer, sa.ForeignKey( 'user.id' ) ),
        sa.Column( 'contact_type', sa.SmallInteger ),
        sa.Column( 'identifier', sa.String(512) )
    )
    op.create_table(
        'shamers',
        sa.Column( 'user', sa.Integer, sa.ForeignKey( 'user.id' ), primary_key=True ),
        sa.Column( 'shamer', sa.Integer, sa.ForeignKey( 'user.id' ), primary_key=True )
    )


def downgrade():
    op.drop_table('shamers')
    op.drop_table('contact_info')
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
