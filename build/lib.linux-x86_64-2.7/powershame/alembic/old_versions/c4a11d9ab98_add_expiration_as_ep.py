"""add expiration as epoch

Revision ID: c4a11d9ab98
Revises: 2048a94d4105
Create Date: 2013-09-04 17:21:58.773612

"""

# revision identifiers, used by Alembic.
revision = 'c4a11d9ab98'
down_revision = '2048a94d4105'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload_creds', sa.Column('expiration', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('upload_creds', 'expiration')
    ### end Alembic commands ###
