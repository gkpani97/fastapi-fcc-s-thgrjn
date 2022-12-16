"""create posts table

Revision ID: 937e24f59745
Revises: 
Create Date: 2022-12-16 11:20:37.879102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937e24f59745'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
