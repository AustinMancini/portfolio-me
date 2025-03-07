"""checking to see if revision still works 2

Revision ID: 299854833d91
Revises: 395fa7244329
Create Date: 2025-02-26 11:57:38.858425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299854833d91'
down_revision: Union[str, None] = '395fa7244329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'profiles', ['author_id'], ['user_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('profiles_user_id_fkey', 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='auth', ondelete='CASCADE')
    op.drop_column('profiles', 'age')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('age', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'profiles', schema='public', type_='foreignkey')
    op.create_foreign_key('profiles_user_id_fkey', 'profiles', 'users', ['user_id'], ['id'], referent_schema='auth', ondelete='CASCADE')
    op.drop_constraint(None, 'posts', schema='public', type_='foreignkey')
    op.create_foreign_key('posts_author_id_fkey', 'posts', 'profiles', ['author_id'], ['user_id'])
    # ### end Alembic commands ###
