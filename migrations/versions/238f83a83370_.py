"""empty message

Revision ID: 238f83a83370
Revises: 1fc883aac40b
Create Date: 2013-12-04 13:05:43.996403

"""

# revision identifiers, used by Alembic.
revision = '238f83a83370'
down_revision = '1fc883aac40b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('unique_shamer_per_user','shamer',['user','email'])


def downgrade():
    op.drop_constraint('unique_shamer_per_user','shamer')
