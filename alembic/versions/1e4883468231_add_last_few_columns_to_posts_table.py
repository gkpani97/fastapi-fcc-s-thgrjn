"""add last few columns to posts table

Revision ID: 1e4883468231
Revises: d1b049c3419f
Create Date: 2022-12-16 16:42:39.450216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e4883468231'
down_revision = 'd1b049c3419f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone= True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
