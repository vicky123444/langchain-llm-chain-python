from langchain_core.runnables import Runnable

from llm_chain_app.chains import build_concept_explainer_chain


def test_chain_uses_prompt_model_and_parser(monkeypatch):
    captured = {}

    class FakeModel(Runnable):
        def __init__(self, *args, **kwargs):
            self.kwargs = kwargs

        def invoke(self, input, config=None, **kwargs):
            captured["messages"] = input
            return "Model output"

    def fake_chat_openai(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeModel(*args, **kwargs)

    monkeypatch.setattr("llm_chain_app.chains.ChatOpenAI", fake_chat_openai)
    monkeypatch.setattr("llm_chain_app.chains.require_api_key", lambda: "test-key")

    chain = build_concept_explainer_chain(model_name="fake-model")
    result = chain.invoke(
        {
            "concept": "Spring Boot Circuit Breaker",
            "audience": "Java microservices developer",
            "detail_level": "Intermediate",
        }
    )

    assert result == "Model output"
    assert captured["kwargs"]["model"] == "fake-model"
    assert "Spring Boot Circuit Breaker" in str(captured["messages"])
