"""Changed charge col to str

Revision ID: d74e8b155442
Revises: 8c12a2cf8824
Create Date: 2022-02-01 01:48:29.670630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d74e8b155442"
down_revision = "8c12a2cf8824"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("shop", "charge_id")
    op.add_column("shop", sa.Column("charge_id", sa.String(), nullable=True))


def downgrade():
    op.drop_column("shop", "charge_id")
    op.add_column("shop", sa.Column("charge_id", sa.Integer(), nullable=True))
