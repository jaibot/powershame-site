"""Removing session shamers

Revision ID: 4bf5bdfeda5
Revises: 3943077a8823
Create Date: 2013-10-14 17:12:25.566579

"""

# revision identifiers, used by Alembic.
revision = '4bf5bdfeda5'
down_revision = '3943077a8823'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(u'session_shamers')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'session_shamers',
    sa.Column(u'session', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column(u'shamer', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['session'], [u'session.id'], name=u'session_shamers_ibfk_1'),
    sa.ForeignKeyConstraint(['shamer'], [u'contact_info.id'], name=u'session_shamers_ibfk_2'),
    sa.PrimaryKeyConstraint(),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
