"""
Context builder for the AI companion.
Retrieves recent journal entries and builds a system prompt
that gives the AI memory of who the user is.
"""
from sqlalchemy.orm import Session
from app.models.journal import Journal
from app.models.chat import ChatMessage
from app.ai.prompt_templates import build_system_prompt, MEMORY_CONTEXT_TEMPLATE, NO_MEMORY_CONTEXT

# How many recent journals to include in context
JOURNAL_MEMORY_LIMIT = 5
# How many recent messages to include in conversation history
CONVERSATION_HISTORY_LIMIT = 20


def build_chat_context(user_id: int, messages: list[ChatMessage], db: Session) -> list[dict]:
    """
    Build the full message list for the AI:
    [system_message, ...recent_chat_messages]

    The system message includes a summary of recent journal entries
    to give the AI memory of the patient's life.
    """
    # Fetch recent journals for memory
    recent_journals = (
        db.query(Journal)
        .filter(Journal.user_id == user_id)
        .order_by(Journal.created_at.desc())
        .limit(JOURNAL_MEMORY_LIMIT)
        .all()
    )

    if recent_journals:
        journal_summaries = "\n".join(
            f"- [{j.created_at.strftime('%B %d, %Y')}] {j.title}: {j.content[:200]}{'...' if len(j.content) > 200 else ''}"
            for j in reversed(recent_journals)
        )
        memory_context = MEMORY_CONTEXT_TEMPLATE.format(journal_summaries=journal_summaries)
    else:
        memory_context = NO_MEMORY_CONTEXT

    system_message = {
        "role": "system",
        "content": build_system_prompt(memory_context),
    }

    # Trim conversation history to avoid exceeding context window
    trimmed_messages = messages[-CONVERSATION_HISTORY_LIMIT:]

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in trimmed_messages
    ]

    return [system_message] + history
