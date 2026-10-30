"""Remove unused diagram and transfer functions from existing databases."""

from alembic import op

revision = "20261011_0023"
down_revision = "20261004_0022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.fn_room_matrix(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_assignment_history(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.fn_transfer_bed(uuid, uuid, uuid, date)")


def downgrade() -> None:
    # Removed features are intentionally not restored.
    pass
