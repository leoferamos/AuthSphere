"""add log:view permission

Revision ID: 5d0bfc241ab7
Revises: 
Create Date: 2025-05-31 16:40:01.005128

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5d0bfc241ab7'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add the log:view permission if it does not exist
    op.execute(
        "INSERT IGNORE INTO permissions (name, description) VALUES ('log:view', 'Allows viewing system logs');"
    )
    # Associate the permission with the admin role
    op.execute(
        """
        INSERT IGNORE INTO role_permissions (role_id, permission_name)
        SELECT r.id, 'log:view'
        FROM roles r
        WHERE r.name = 'admin';
        """
    )

def downgrade():
    # Remove the association and the permission (rollback)
    op.execute(
        "DELETE FROM role_permissions WHERE permission_name = 'log:view';"
    )
    op.execute(
        "DELETE FROM permissions WHERE name = 'log:view';"
    )
