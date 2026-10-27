from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from .config import get_model_name, require_api_key
from .prompts import build_prompt_template


def build_concept_explainer_chain(model_name: str | None = None, temperature: float = 0.2):
    """Build the prompt -> model -> parser pipeline."""
    resolved_model = model_name or get_model_name()
    require_api_key()

    prompt = build_prompt_template()
    model = ChatOpenAI(model=resolved_model, temperature=temperature)
    parser = StrOutputParser()

    return prompt | model | parser


__all__ = ["build_concept_explainer_chain"]
