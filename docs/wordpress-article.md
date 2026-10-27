# LangChain Explained for Developers: Build Your First LLM Chain with Python

LangChain helps developers compose model calls into reusable application pipelines. In this hands-on guide, we will build a small Python command-line application that turns a technology concept into a developer-friendly explanation. The project demonstrates one core pattern: a prompt template, a chat model, and an output parser connected into a reusable chain.

**Project source:** [langchain-llm-chain-python on GitHub](https://github.com/vicky123444/langchain-llm-chain-python)

**What we will build:** a Technical Concept Explainer. Provide a concept such as “Spring Boot Circuit Breaker,” the target audience, and the detail level. The chain asks the model to produce a definition, explain how it works, show a practical example, and list common pitfalls.

## 1. What is LangChain?

LangChain is a framework for composing the parts of an LLM application. In this beginner-friendly project, we use three components:

- **Prompt template:** defines the task and the input variables.
- **Chat model:** sends the formatted messages to a model provider.
- **Output parser:** converts the model response into a convenient representation, in this case plain text.

LangChain Core provides the abstractions used to compose these building blocks, while the OpenAI integration package provides `ChatOpenAI`. The packages are modular, so a provider integration is installed separately. See the [LangChain Core reference](https://reference.langchain.com/python/langchain-core) and [LangChain OpenAI reference](https://reference.langchain.com/python/langchain-openai/langchain_openai).

## 2. Why build a chain instead of one direct call?

A direct model call can be useful for a quick experiment. A reusable chain makes the pipeline’s responsibilities visible and repeatable. The prompt can be updated without changing the CLI, and the model can be mocked when testing the chain’s wiring. The same pattern can later be extended with structured output, retrieval, batching, or streaming.

## 3. Project overview

```text
langchain-llm-chain-python/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── src/
│   └── llm_chain_app/
│       ├── config.py
│       ├── prompts.py
│       ├── chains.py
│       └── cli.py
├── tests/
│   ├── test_prompts.py
│   └── test_chain.py
├── docs/architecture.md
└── .github/workflows/tests.yml
```

`config.py` loads configuration, `prompts.py` defines the prompt, `chains.py` composes the components, and `cli.py` accepts command-line inputs. The tests cover prompt construction and the chain flow without calling a live LLM.

## 4. Prerequisites and installation

You need Python 3.10–3.12, an OpenAI API key, and access to a model available to your API account. Clone the repository:

```bash
git clone https://github.com/vicky123444/langchain-llm-chain-python.git
cd langchain-llm-chain-python
```

Create a virtual environment.

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and the local package:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

The project uses `langchain-core`, `langchain-openai`, `python-dotenv`, and `pytest`. See the [OpenAI chat integration guide](https://docs.langchain.com/oss/python/integrations/chat/openai).

## 5. Configure the API key safely

Copy the sample environment file:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Then edit `.env` on your own machine:

```dotenv
OPENAI_API_KEY=replace-with-your-own-api-key
OPENAI_MODEL=gpt-4o-mini
```

Do not commit the real `.env` file, expose the key in screenshots, or paste it into source code. The repository’s `.gitignore` excludes `.env`. Model availability and price can change; check your current provider account settings.

## 6. Define the prompt template

In `src/llm_chain_app/prompts.py`, we use `ChatPromptTemplate` to name the inputs and request a consistent response structure:

```python
from langchain_core.prompts import ChatPromptTemplate


def build_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
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
    ])
```

The template separates the reusable instruction from the values supplied each time. The variable names in the prompt must match the keys passed into `invoke()`. See the [ChatPromptTemplate API reference](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate).

## 7. Build the LLM chain

The central implementation lives in `src/llm_chain_app/chains.py`:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from .config import get_model_name, require_api_key
from .prompts import build_prompt_template


def build_concept_explainer_chain(model_name: str | None = None, temperature: float = 0.2):
    resolved_model = model_name or get_model_name()
    require_api_key()

    prompt = build_prompt_template()
    model = ChatOpenAI(model=resolved_model, temperature=temperature)
    parser = StrOutputParser()

    return prompt | model | parser
```

The line `prompt | model | parser` composes compatible LangChain runnables. First the prompt receives a dictionary and renders chat messages. The model generates a response. Then the parser extracts plain text, giving the caller one simple string. The pipe operator reduces glue code and keeps the flow easy to understand.

## 8. Run the concept explainer

Run the CLI from the repository root:

```bash
python -m llm_chain_app.cli \
  --concept "Spring Boot Circuit Breaker" \
  --audience "Java microservices developer" \
  --detail-level "Intermediate"
```

The command prints the model response. A typical response contains a definition of the Circuit Breaker pattern, an explanation of how a breaker tracks failures and prevents repeated calls to an unhealthy dependency, a practical Java microservices use case, and pitfalls such as confusing circuit breakers with retries. The wording and details vary by model; validate technical recommendations before applying them.

## 9. Test without a live model call

Run:

```bash
pytest
```

The prompt tests verify the expected variables and sections. The chain test substitutes a fake LangChain `Runnable` for the live model, so you can test the composition without an API key or model usage cost. GitHub Actions is configured to run the tests on Python 3.10, 3.11, and 3.12.

## 10. Troubleshooting and best practices

- **Missing API key:** check that `.env` exists in the project root and contains your own key.
- **Import error:** activate the virtual environment and run `pip install -e .`.
- **Authentication or quota error:** check the key, billing status, network, and model access. Avoid uncontrolled retries that may increase cost.
- **Incorrect response:** LLM output is not guaranteed to be correct. Verify technical claims against official documentation or other trusted sources.

For production, add input validation, timeouts, bounded retries, rate limits, structured logging, usage monitoring, and evaluation. Do not send confidential data to a hosted model unless your organization permits it.

## Key takeaway

LangChain’s core value in this example is composition. A reusable prompt, a model integration, and an output parser become one chain that accepts clear inputs and returns clear text. Once this small pattern is understood, it is easier to build structured-output chains, multi-step workflows, and RAG applications.

## Official references

- [LangChain documentation](https://docs.langchain.com/)
- [LangChain Core reference](https://reference.langchain.com/python/langchain-core)
- [ChatPromptTemplate reference](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [OpenAI chat integration guide](https://docs.langchain.com/oss/python/integrations/chat/openai)
- [LangChain OpenAI API reference](https://reference.langchain.com/python/langchain-openai/langchain_openai)

## Project source code

Browse the complete project source on [GitHub: langchain-llm-chain-python](https://github.com/vicky123444/langchain-llm-chain-python).
