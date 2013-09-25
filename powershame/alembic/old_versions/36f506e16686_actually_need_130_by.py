"""actually need 130 bytes for pw...sigh

Revision ID: 36f506e16686
Revises: 23621d8cb290
Create Date: 2013-07-12 22:22:58.217028

"""

# revision identifiers, used by Alembic.
revision = '36f506e16686'
down_revision = '23621d8cb290'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(table_name='user',column_name='password',type_=sa.Unicode(130))
    pass


def downgrade():
    op.alter_column(table_name='user',column_name='password',type_=sa.Unicode(128))
    pass
