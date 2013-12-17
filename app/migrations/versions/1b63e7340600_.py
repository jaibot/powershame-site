"""empty message

Revision ID: 1b63e7340600
Revises: 32dd278f60f0
Create Date: 2013-10-30 04:06:04.468462

"""

# revision identifiers, used by Alembic.
revision = '1b63e7340600'
down_revision = '32dd278f60f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('screenshot', sa.Column('upload_args', sa.Unicode(2048), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('screenshot', 'upload_args')
    ### end Alembic commands ###
