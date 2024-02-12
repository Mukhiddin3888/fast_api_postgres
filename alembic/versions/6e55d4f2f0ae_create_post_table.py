"""create post table

Revision ID: 6e55d4f2f0ae
Revises: 
Create Date: 2024-02-12 14:14:07.965562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e55d4f2f0ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(): 
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), 
                    sa.Column('title', sa.String, nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
