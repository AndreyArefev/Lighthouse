import sqlalchemy_utils

"""V.1

Revision ID: 7b514a062d32
Revises: 
Create Date: 2023-04-08 17:02:34.605026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b514a062d32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id_category', sa.Integer(), nullable=False),
    sa.Column('name_category', sa.String(), nullable=False, unique=True),
    sa.PrimaryKeyConstraint('id_category')
    )
    op.create_table('tags',
    sa.Column('id_tag', sa.Integer(), nullable=False),
    sa.Column('name_tag', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id_tag')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('phone', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=12), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id_event', sa.Integer(), nullable=False),
    sa.Column('name_event', sa.String(length=200), nullable=False),
    sa.Column('id_category', sa.Integer(), nullable=True),
    sa.Column('time_event', sa.TIMESTAMP(), nullable=True),
    sa.Column('place_event', sa.String(), nullable=True),
    sa.Column('about_event', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('age_limit', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('id_organizer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_category'], ['category.id_category'], ),
    sa.ForeignKeyConstraint(['id_organizer'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_event')
    )
    op.create_table('tableEventTag',
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('tag', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event'], ['event.id_event'], ),
    sa.ForeignKeyConstraint(['tag'], ['tag.id_tag'], ),
    sa.PrimaryKeyConstraint('event', 'tag')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table_event_tag')
    op.drop_table('events')
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('categories')
    # ### end Alembic commands ###
