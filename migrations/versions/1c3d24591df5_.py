"""empty message

Revision ID: 1c3d24591df5
Revises: efc4551164db
Create Date: 2019-02-05 17:28:10.727105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c3d24591df5'
down_revision = 'efc4551164db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slack_bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bot_user_id', sa.String(), nullable=True),
    sa.Column('bot_access_token', sa.String(), nullable=True),
    sa.Column('team_name', sa.String(), nullable=True),
    sa.Column('team_id', sa.String(), nullable=True),
    sa.Column('_scopes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('user_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_name')
    op.drop_table('slack_bots')
    # ### end Alembic commands ###
