"""adding s3 creds

Revision ID: 256a41ae2e2
Revises: 108644ea05a8
Create Date: 2013-08-05 13:48:41.292718

"""

# revision identifiers, used by Alembic.
revision = '256a41ae2e2'
down_revision = '108644ea05a8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'upload_creds',
        sa.Column( 'id', sa.Integer, primary_key=True ),
        sa.Column( 'user', sa.Integer, sa.ForeignKey('user.id'), index=True ),
        sa.Column( 'expiration', sa.DateTime ),
        sa.Column( 'access_id', sa.String(256) ),
        sa.Column( 'secret_key', sa.String(256) ),
        sa.Column( 'session_token', sa.String(2048) )
    )

def downgrade():
    op.drop_table( 'upload_creds' )
