"""rank attribute

Revision ID: 4a1cf601bead
Revises: d9dd35b76417
Create Date: 2022-06-18 12:34:52.264611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1cf601bead'
down_revision = 'd9dd35b76417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('rank', sa.Integer(), nullable=False))
    op.add_column('notebook', sa.Column('rank', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notebook', 'rank')
    op.drop_column('note', 'rank')
    # ### end Alembic commands ###
