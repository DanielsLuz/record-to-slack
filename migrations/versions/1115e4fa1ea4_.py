"""empty message

Revision ID: 1115e4fa1ea4
Revises: f491bcd881e1
Create Date: 2019-01-23 20:35:29.266744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1115e4fa1ea4'
down_revision = 'f491bcd881e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client_token', sa.Column('_scopes', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client_token', '_scopes')
    # ### end Alembic commands ###
