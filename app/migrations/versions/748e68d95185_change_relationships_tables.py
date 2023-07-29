"""change relationships tables

Revision ID: 748e68d95185
Revises: 02b484d6c1cf
Create Date: 2023-07-21 08:36:34.698530

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "748e68d95185"
down_revision = "02b484d6c1cf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("relationship_types")
    op.add_column(
        "users_relationships",
        sa.Column("relationship_status", sa.String(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users_relationships", "relationship_status")
    op.create_table(
        "relationship_types",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "relationship_status",
            postgresql.ENUM(
                "FRIENDS", "SUBSCRIBER", "SEND_FRIEND_REQUEST", name="relationshiptypes"
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="relationship_types_pkey"),
        sa.UniqueConstraint(
            "relationship_status", name="relationship_types_relationship_status_key"
        ),
    )
    # ### end Alembic commands ###
