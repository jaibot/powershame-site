"""tweaking

Revision ID: df7331a2aab
Revises: 42076a1fa52c
Create Date: 2013-08-08 15:51:06.795396

"""

# revision identifiers, used by Alembic.
revision = 'df7331a2aab'
down_revision = '42076a1fa52c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column( 'session', 'user_id' )

def downgrade():
    pass
