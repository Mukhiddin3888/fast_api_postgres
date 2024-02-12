"""create user table

Revision ID: 9ccd08fd4b75
Revises: b170c8fad1c1
Create Date: 2024-02-12 15:54:14.828397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ccd08fd4b75'
down_revision: Union[str, None] = 'b170c8fad1c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', 
                              sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
                    
                
                    )
    
    pass


def downgrade():
    op.drop_table('users')
    pass
