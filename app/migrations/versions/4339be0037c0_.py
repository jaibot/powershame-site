"""empty message

Revision ID: 4339be0037c0
Revises: 557d03b2f29e
Create Date: 2014-01-24 06:32:46.319245

"""

# revision identifiers, used by Alembic.
revision = '4339be0037c0'
down_revision = '557d03b2f29e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("session","height",server_default="768")
    op.alter_column("session","width",server_default="1024")


def downgrade():
    op.alter_column( "session", "height", server_default = None)
    op.alter_column( "session", "width", server_default = None)
