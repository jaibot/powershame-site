"""create account table

Revision ID: fde787ea41b
Revises: None
Create Date: 2013-07-11 10:47:28.700253

"""

# revision identifiers, used by Alembic.
revision = 'fde787ea41b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'account',
            sa.Column('id',sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('description',sa.Unicode(200) )
)


def downgrade():
    op.drop_table('account')
