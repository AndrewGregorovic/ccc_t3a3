"""Initial migration

Revision ID: 03e781178ab1
Revises: 
Create Date: 2020-12-18 14:08:48.782724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03e781178ab1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=20), nullable=False),
    sa.Column('href', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('popularity', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=20), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=True),
    sa.Column('display_name', sa.String(length=30), nullable=True),
    sa.Column('href', sa.String(), nullable=False),
    sa.Column('product', sa.String(length=20), nullable=False),
    sa.Column('object_type', sa.String(length=20), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_type', sa.String(length=20), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('copyright', sa.String(length=100), nullable=False),
    sa.Column('copyright_type', sa.String(length=1), nullable=False),
    sa.Column('genre', sa.String(length=20), nullable=False),
    sa.Column('href', sa.String(), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('release_date', sa.Integer(), nullable=False),
    sa.Column('release_date_precision', sa.String(length=5), nullable=False),
    sa.Column('object_type', sa.String(length=20), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tracks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('disc_number', sa.Integer(), nullable=True),
    sa.Column('duration_ms', sa.Integer(), nullable=False),
    sa.Column('explicit', sa.Boolean(), nullable=False),
    sa.Column('href', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('popularity', sa.Integer(), nullable=False),
    sa.Column('preview_url', sa.String(), nullable=False),
    sa.Column('track_number', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=20), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.Column('is_local', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('track_ratings',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'track_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_ratings')
    op.drop_table('tracks')
    op.drop_table('albums')
    op.drop_table('users')
    op.drop_table('artists')
    op.drop_table('admin')
    # ### end Alembic commands ###
