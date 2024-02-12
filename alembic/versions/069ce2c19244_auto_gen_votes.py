"""auto gen votes

Revision ID: 069ce2c19244
Revises: 95247c624cd1
Create Date: 2024-02-12 17:18:48.398585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '069ce2c19244'
down_revision: Union[str, None] = '95247c624cd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer, nullable=False, ),
                    sa.Column('post_id', sa.Integer, nullable=False, ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    
                    )
    pass


def downgrade():
    op.drop_table('votes')
    pass
