"""empty message

Revision ID: 10ecf78c7c5d
Revises: f21b347b57a1
Create Date: 2021-11-28 00:12:38.835892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '10ecf78c7c5d'
down_revision = 'f21b347b57a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.drop_constraint('member_role_fkey', 'member', type_='foreignkey')
    op.create_foreign_key(None, 'member', 'role', ['role_id'], ['id'])
    op.drop_column('member', 'role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('role', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'member', type_='foreignkey')
    op.create_foreign_key('member_role_fkey', 'member', 'role', ['role'], ['id'])
    op.drop_column('member', 'role_id')
    # ### end Alembic commands ###