"""merge logs set null and logs table

Revision ID: 0d67d4a9dbd9
Revises: 2d312773e6aa, xxxx_set_null_logs_user_id
Create Date: 2025-06-01 01:07:20.914824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d67d4a9dbd9'
down_revision = ('2d312773e6aa', 'xxxx_set_null_logs_user_id')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
