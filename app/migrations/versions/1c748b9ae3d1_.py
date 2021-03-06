"""empty message

Revision ID: 1c748b9ae3d1
Revises: 1ace0afcd10
Create Date: 2014-02-21 15:53:18.077814

"""

# revision identifiers, used by Alembic.
revision = '1c748b9ae3d1'
down_revision = '1ace0afcd10'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'unique_shamer_per_user', 'shamer')
    #op.drop_index('unique_shamer_per_user', table_name='shamer')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    #op.create_index('unique_shamer_per_user', 'shamer', ['user', 'email'], unique=True)
    op.create_unique_constraint(u'unique_shamer_per_user', 'shamer', ['user', 'email'])
    ### end Alembic commands ###
