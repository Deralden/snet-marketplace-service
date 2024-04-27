"""add training_indicator

Revision ID: 15bbbaaba5f7
Revises: 57deaf9ab42f
Create Date: 2024-03-22 12:19:51.299812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15bbbaaba5f7'
down_revision = '57deaf9ab42f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('training_indicator', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'training_indicator')
    # ### end Alembic commands ###
