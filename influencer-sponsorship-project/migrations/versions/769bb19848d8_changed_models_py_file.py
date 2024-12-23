"""Changed models.py file

Revision ID: 769bb19848d8
Revises: 
Create Date: 2024-08-12 16:30:19.607699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '769bb19848d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flags', schema=None) as batch_op:
        batch_op.add_column(sa.Column('flag_user_type', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flags', schema=None) as batch_op:
        batch_op.drop_column('flag_user_type')

    # ### end Alembic commands ###
