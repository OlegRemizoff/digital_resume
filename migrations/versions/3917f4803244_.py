"""empty message

Revision ID: 3917f4803244
Revises: 75f52872bf50
Create Date: 2023-02-12 10:21:55.677565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3917f4803244'
down_revision = '75f52872bf50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
