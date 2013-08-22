"""add prefixes to upload creds

Revision ID: 220b262e2716
Revises: 256a41ae2e2
Create Date: 2013-08-06 14:42:07.487982

"""

# revision identifiers, used by Alembic.
revision = '220b262e2716'
down_revision = '256a41ae2e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column( 
        'upload_creds',
        sa.Column( 'prefix', sa.String(256) )
    )


def downgrade():
    op.drop_column(
        'upload_creds',
        'prefix'
    )
