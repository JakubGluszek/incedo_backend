"""drop daily notes

Revision ID: d9dd35b76417
Revises: f227527bf381
Create Date: 2022-06-18 12:23:15.120939

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd9dd35b76417'
down_revision = 'f227527bf381'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dailynote')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dailynote',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='dailynote_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='dailynote_pkey')
    )
    # ### end Alembic commands ###
