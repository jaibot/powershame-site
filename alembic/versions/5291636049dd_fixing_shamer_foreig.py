"""fixing shamer foreignkeys

Revision ID: 5291636049dd
Revises: c4f2a3d329e
Create Date: 2013-07-31 15:14:26.699600

"""

# revision identifiers, used by Alembic.
revision = '5291636049dd'
down_revision = 'c4f2a3d329e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('shamers')


def downgrade():
    op.drop_table('shamers')
