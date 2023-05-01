"""init users db

Revision ID: 868ba78933c4
Revises:
Create Date: 2023-03-28 02:29:06.396929

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op


# revision identifiers, used by Alembic.
revision = "868ba78933c4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "roles",
            sa.ARRAY(
                sa.Enum(
                    "ROLE_USER",
                    "ROLE_MODERATOR",
                    "ROLE_ADMIN",
                    "ROLE_SUPERADMIN",
                    name="userrole",
                )
            ),
            nullable=True,
        ),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=15), nullable=False),
        sa.Column(
            "surname", sqlmodel.sql.sqltypes.AutoString(length=15), nullable=False
        ),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
