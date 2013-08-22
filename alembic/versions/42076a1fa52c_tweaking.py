"""tweaking

Revision ID: 42076a1fa52c
Revises: 19958bde13a0
Create Date: 2013-08-08 15:49:03.548043

"""

# revision identifiers, used by Alembic.
revision = '42076a1fa52c'
down_revision = '19958bde13a0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    pass


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column(u'user', mysql.INTEGER(display_width=11), nullable=True))
    op.drop_column('session', 'user_id')
    ### end Alembic commands ###
