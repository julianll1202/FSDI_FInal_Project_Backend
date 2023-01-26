"""users table change


Revision ID: c7fa8fa74240
Revises: 89bf043b7e0d
Create Date: 2023-01-25 10:06:45.798562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7fa8fa74240'
down_revision = '89bf043b7e0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=10), nullable=True))
        batch_op.drop_index('ix_user_name')
        batch_op.create_index(batch_op.f('ix_user_first_name'), ['first_name'], unique=False)
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=10), nullable=True))
        batch_op.drop_index(batch_op.f('ix_user_first_name'))
        batch_op.create_index('ix_user_name', ['name'], unique=False)
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
