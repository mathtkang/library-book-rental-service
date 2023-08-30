"""Move rental_num from user model to rent model

Revision ID: b2b24cc4e012
Revises: ac4be06a2e46
Create Date: 2023-08-30 19:37:36.424432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b2b24cc4e012'
down_revision = 'ac4be06a2e46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rental_num', sa.Integer(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('rental_num')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rental_num', mysql.INTEGER(), autoincrement=False, nullable=True))

    with op.batch_alter_table('rent', schema=None) as batch_op:
        batch_op.drop_column('rental_num')

    # ### end Alembic commands ###
