from alembic import op
import sqlalchemy as sa

revision = 'xxxx_set_null_logs_user_id'
down_revision = 'a6b07c74c303'  # ajuste para a sua última migration real
branch_labels = None
depends_on = None

def upgrade():
    # Remove a FK antiga
    op.drop_constraint('logs_ibfk_1', 'logs', type_='foreignkey')
    # Permite user_id ser NULL
    op.alter_column('logs', 'user_id', existing_type=sa.String(length=36), nullable=True)
    # Cria nova FK com ON DELETE SET NULL
    op.create_foreign_key(
        'logs_ibfk_1', 'logs', 'users', ['user_id'], ['id'], ondelete='SET NULL'
    )

def downgrade():
    op.drop_constraint('logs_ibfk_1', 'logs', type_='foreignkey')
    op.alter_column('logs', 'user_id', existing_type=sa.String(length=36), nullable=False)
    op.create_foreign_key(
        'logs_ibfk_1', 'logs', 'users', ['user_id'], ['id']
    )