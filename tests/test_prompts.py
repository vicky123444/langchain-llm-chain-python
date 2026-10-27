from llm_chain_app.prompts import build_prompt_template


def test_prompt_template_contains_expected_variables():
    prompt = build_prompt_template()
    template = prompt.messages[1].prompt.template

    assert "{concept}" in template
    assert "{audience}" in template
    assert "{detail_level}" in template
    assert "Definition" in template
    assert "How it works" in template
    assert "Practical example" in template
    assert "Common pitfalls" in template


def test_prompt_template_invoke_returns_expected_values():
    prompt = build_prompt_template()
    result = prompt.invoke(
        {
            "concept": "Spring Boot Circuit Breaker",
            "audience": "Java microservices developer",
            "detail_level": "Intermediate",
        }
    )

    assert "Spring Boot Circuit Breaker" in result.to_string()
    assert "Java microservices developer" in result.to_string()
    assert "Intermediate" in result.to_string()
