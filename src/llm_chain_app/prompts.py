from langchain_core.prompts import ChatPromptTemplate


def build_prompt_template() -> ChatPromptTemplate:
    """Create the reusable prompt template for a concept explainer."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a senior developer educator. Explain a technology concept clearly for a developer audience.",
            ),
            (
                "user",
                "Explain the following concept in a practical way.\n"
                "Concept: {concept}\n"
                "Audience: {audience}\n"
                "Detail level: {detail_level}\n\n"
                "Return exactly four sections in this order:\n"
                "1. Definition\n"
                "2. How it works\n"
                "3. Practical example\n"
                "4. Common pitfalls\n"
                "Use concise but helpful developer-focused language.",
            ),
        ]
    )
