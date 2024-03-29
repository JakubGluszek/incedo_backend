"""init

Revision ID: d5fc19f9231a
Revises: 
Create Date: 2022-07-18 11:55:55.348983

"""
from alembic import op
import sqlalchemy as sa

from app.core.config import settings


# revision identifiers, used by Alembic.
revision = 'd5fc19f9231a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('edited_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('primary', sa.String(length=7), nullable=False),
    sa.Column('secondary', sa.String(length=7), nullable=False),
    sa.Column('accent', sa.String(length=7), nullable=False),
    sa.Column('neutral', sa.String(length=7), nullable=False),
    sa.Column('base', sa.String(length=7), nullable=False),
    sa.Column('info', sa.String(length=7), nullable=False),
    sa.Column('success', sa.String(length=7), nullable=False),
    sa.Column('warning', sa.String(length=7), nullable=False),
    sa.Column('error', sa.String(length=7), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=32), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), server_default='hooman', nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('avatar', sa.String(length=512), server_default=f'{settings.HOST}/static/images/avatars/default.png', nullable=False),
    sa.Column('is_super', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('usersettings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_diff', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usersettings')
    op.drop_table('user')
    op.drop_table('token')
    op.drop_table('theme')
    op.drop_table('note')
    # ### end Alembic commands ###
