"""Added tables unique

Revision ID: c658e20055dc
Revises: 8182bba776ef
Create Date: 2025-02-24 22:50:02.809372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c658e20055dc'
down_revision: Union[str, None] = '8182bba776ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'posts', ['id'], schema='public')
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'profiles', ['author_id'], ['user_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('profiles_user_id_fkey', 'profiles', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('profiles_user_id_fkey', 'profiles', 'users', ['user_id'], ['id'], referent_schema='auth', onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'posts', schema='public', type_='foreignkey')
    op.create_foreign_key('posts_author_id_fkey', 'posts', 'profiles', ['author_id'], ['user_id'])
    op.drop_constraint(None, 'posts', schema='public', type_='unique')
    # ### end Alembic commands ###
