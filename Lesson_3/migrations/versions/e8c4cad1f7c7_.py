"""empty message

Revision ID: e8c4cad1f7c7
Revises: a8f290c41ae8
Create Date: 2024-01-11 11:25:56.192613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8c4cad1f7c7'
down_revision = 'a8f290c41ae8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('subject_name', sa.String(length=100), nullable=True),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mark')
    # ### end Alembic commands ###
