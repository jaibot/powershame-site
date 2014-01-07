"""empty message

Revision ID: 318f16b6da32
Revises: 62e7aa694d3
Create Date: 2013-11-07 03:13:01.290453

"""

# revision identifiers, used by Alembic.
revision = '318f16b6da32'
down_revision = '62e7aa694d3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session', sa.Integer(), nullable=True),
    sa.Column('shamer', sa.Integer(), nullable=True),
    sa.Column('secret', sa.Unicode(length=64), nullable=True),
    sa.ForeignKeyConstraint(['session'], ['session.id'], ),
    sa.ForeignKeyConstraint(['shamer'], ['shamer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('secret')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_view')
    ### end Alembic commands ###