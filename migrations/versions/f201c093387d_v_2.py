import sqlalchemy_utils

"""v.2

Revision ID: f201c093387d
Revises: 7b514a062d32
Create Date: 2023-04-14 01:03:46.909844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f201c093387d'
down_revision = '7b514a062d32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('table_event_tag')
    op.create_table('tableEventTag',
                    sa.Column('event', sa.Integer(), nullable=False),
                    sa.Column('tag', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['event'], ['event.id_event'], ),
                    sa.ForeignKeyConstraint(['tag'], ['tag.id_tag'], ),
                    sa.PrimaryKeyConstraint('event', 'tag')
                    )


def downgrade() -> None:
    pass
