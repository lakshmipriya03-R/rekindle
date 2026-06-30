"""Initial schema — create all tables

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"])

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_refresh_tokens_token", "refresh_tokens", ["token"], unique=True)
    op.create_index("ix_refresh_tokens_id", "refresh_tokens", ["id"])

    op.create_table(
        "journals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("mood_score", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_journals_id", "journals", ["id"])
    op.create_index("ix_journals_user_id", "journals", ["user_id"])
    op.create_index("ix_journals_created_at", "journals", ["created_at"])

    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_sessions_id", "conversation_sessions", ["id"])
    op.create_index("ix_conversation_sessions_user_id", "conversation_sessions", ["user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["conversation_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chat_messages_id", "chat_messages", ["id"])
    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])
    op.create_index("ix_chat_messages_created_at", "chat_messages", ["created_at"])

    op.create_table(
        "emotion_analyses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("journal_id", sa.Integer(), nullable=True),
        sa.Column("chat_message_id", sa.Integer(), nullable=True),
        sa.Column(
            "source_type",
            sa.Enum("journal", "chat", name="sourcetype"),
            nullable=False,
        ),
        sa.Column(
            "dominant_emotion",
            sa.Enum("joy", "sadness", "fear", "anger", "surprise", "disgust", "neutral", name="emotionlabel"),
            nullable=False,
        ),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("joy_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("sadness_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("fear_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("anger_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("surprise_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("disgust_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("neutral_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["journal_id"], ["journals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["chat_message_id"], ["chat_messages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_emotion_analyses_id", "emotion_analyses", ["id"])
    op.create_index("ix_emotion_analyses_user_id", "emotion_analyses", ["user_id"])
    op.create_index("ix_emotion_analyses_journal_id", "emotion_analyses", ["journal_id"])
    op.create_index("ix_emotion_analyses_dominant_emotion", "emotion_analyses", ["dominant_emotion"])
    op.create_index("ix_emotion_analyses_analyzed_at", "emotion_analyses", ["analyzed_at"])


def downgrade() -> None:
    op.drop_table("emotion_analyses")
    op.drop_table("chat_messages")
    op.drop_table("conversation_sessions")
    op.drop_table("journals")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
