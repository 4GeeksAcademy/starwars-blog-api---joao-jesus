"""empty message

Revision ID: e00029325f41
Revises: 65405ff93601
Create Date: 2024-04-25 15:33:04.737922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e00029325f41'
down_revision = '65405ff93601'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('heigth')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('diameter',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('gravity',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('gravity',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('diameter',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('heigth', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('user_id')
        batch_op.drop_column('height')

    # ### end Alembic commands ###