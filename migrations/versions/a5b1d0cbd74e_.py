"""empty message

Revision ID: a5b1d0cbd74e
Revises: 4441530d6b8f
Create Date: 2019-05-30 09:07:24.255885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5b1d0cbd74e'
down_revision = '4441530d6b8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo', sa.Column('caption', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo', 'caption')
    # ### end Alembic commands ###