"""init_tables

Revision ID: bed0a38a7361
Revises: e48471771a89
Create Date: 2021-04-01 06:52:05.965666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bed0a38a7361'
down_revision = 'e48471771a89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('is_show', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('name', table_name='area')
    op.drop_index('imgs', table_name='gallery')
    op.drop_constraint('gallery_ibfk_1', 'gallery', type_='foreignkey')
    op.create_foreign_key(None, 'gallery', 'project', ['project_id'], ['id'], ondelete='cascade')
    op.drop_index('image', table_name='type')
    op.drop_index('name', table_name='type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'type', ['name'], unique=True)
    op.create_index('image', 'type', ['image'], unique=True)
    op.drop_constraint(None, 'gallery', type_='foreignkey')
    op.create_foreign_key('gallery_ibfk_1', 'gallery', 'project', ['project_id'], ['id'])
    op.create_index('imgs', 'gallery', ['imgs'], unique=True)
    op.create_index('name', 'area', ['name'], unique=True)
    op.drop_table('chat')
    # ### end Alembic commands ###