"""initial migration

Revision ID: c16bc9fb2d6a
Revises: 44c996f0490d
Create Date: 2023-11-10 02:13:43.877117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c16bc9fb2d6a'
down_revision: Union[str, None] = '44c996f0490d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('password', sa.String(length=255), nullable=True))
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'user', ['username'])
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'password')
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###
