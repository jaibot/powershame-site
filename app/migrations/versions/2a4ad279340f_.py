"""empty message

Revision ID: 2a4ad279340f
Revises: 238f83a83370
Create Date: 2013-12-04 14:50:30.372138

"""

# revision identifiers, used by Alembic.
revision = '2a4ad279340f'
down_revision = '238f83a83370'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shamer', sa.Column('end_notifications', sa.Boolean(), nullable=True))
    op.add_column('shamer', sa.Column('start_notifications', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shamer', 'start_notifications')
    op.drop_column('shamer', 'end_notifications')
    ### end Alembic commands ###
