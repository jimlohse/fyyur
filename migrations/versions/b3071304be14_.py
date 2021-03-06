"""empty message

Revision ID: b3071304be14
Revises: 8fbb681fc20e
Create Date: 2021-07-20 14:25:18.369225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3071304be14'
down_revision = '8fbb681fc20e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
