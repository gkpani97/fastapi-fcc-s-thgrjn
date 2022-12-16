"""add content column to posts table

Revision ID: fd1be5ad6764
Revises: 937e24f59745
Create Date: 2022-12-16 12:15:41.614065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd1be5ad6764'
down_revision = '937e24f59745'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
