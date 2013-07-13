"""switch to unicode

Revision ID: 56e693da8cfd
Revises: 1ae85abf9b95
Create Date: 2013-07-12 17:03:31.062060

"""

# revision identifiers, used by Alembic.
revision = '56e693da8cfd'
down_revision = '1ae85abf9b95'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(table_name='user',column_name='username',type_=sa.Unicode(32))
    op.alter_column(table_name='user',column_name='password',type_=sa.Unicode(64))
    pass


def downgrade():
    pass
