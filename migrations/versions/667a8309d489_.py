"""empty message

Revision ID: 667a8309d489
Revises: 82830b32da5a
Create Date: 2023-02-01 20:54:08.065662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '667a8309d489'
down_revision = '82830b32da5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('food', schema=None) as batch_op:
        batch_op.drop_index('ix_food_food_name')
        batch_op.create_index(batch_op.f('ix_food_food_name'), ['food_name'], unique=False)

    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.drop_index('ix_restaurant_restaurant_name')
        batch_op.create_index(batch_op.f('ix_restaurant_restaurant_name'), ['restaurant_name'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_email')
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.create_index('ix_user_email', ['email'], unique=False)

    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_restaurant_restaurant_name'))
        batch_op.create_index('ix_restaurant_restaurant_name', ['restaurant_name'], unique=False)

    with op.batch_alter_table('food', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_food_food_name'))
        batch_op.create_index('ix_food_food_name', ['food_name'], unique=False)

    # ### end Alembic commands ###
