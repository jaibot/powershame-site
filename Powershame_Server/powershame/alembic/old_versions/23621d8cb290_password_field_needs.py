"""password field needs to hold at least 86 chars

Revision ID: 23621d8cb290
Revises: 56e693da8cfd
Create Date: 2013-07-12 20:00:09.812658

"""

# revision identifiers, used by Alembic.
revision = '23621d8cb290'
down_revision = '56e693da8cfd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(table_name='user',column_name='password',type_=sa.Unicode(128))
    pass


def downgrade():
    pass
