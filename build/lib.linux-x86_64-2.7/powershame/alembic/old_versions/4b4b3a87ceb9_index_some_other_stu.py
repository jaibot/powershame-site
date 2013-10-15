"""index some other stuff

Revision ID: 4b4b3a87ceb9
Revises: 291c1b6e962d
Create Date: 2013-08-08 12:01:17.569358

"""

# revision identifiers, used by Alembic.
revision = '4b4b3a87ceb9'
down_revision = '291c1b6e962d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index( 'usernames', 'user', ['username'] )


def downgrade():
    op.drop_index( 'usernames' )
