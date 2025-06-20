"""fix models

Revision ID: a6b07c74c303
Revises: a0cb52818fe0
Create Date: 2025-05-31 23:37:06.351138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6b07c74c303'
down_revision = 'a0cb52818fe0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form_fields', schema=None) as batch_op:
        batch_op.alter_column('is_required',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
        batch_op.alter_column('is_active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
        batch_op.alter_column('field_type',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('form_fields', schema=None) as batch_op:
        batch_op.alter_column('field_type',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('is_active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
        batch_op.alter_column('is_required',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)

    # ### end Alembic commands ###
