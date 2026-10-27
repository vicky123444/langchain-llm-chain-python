# Architecture overview

The application deliberately uses a simple sequence of LangChain components so each stage can be inspected and tested independently.

## Flow

1. The CLI parses the concept, audience, and detail level.
2. \`ChatPromptTemplate\` formats the input into system and user messages.
3. \`ChatOpenAI\` invokes the selected OpenAI chat model.
4. \`StrOutputParser\` extracts plain text from the model response.
5. The CLI prints the explanation for the developer.

## Component responsibilities

- \`config.py\` loads \`.env\`, returns the configured model name, and checks that an API key is present.
- \`prompts.py\` owns the reusable prompt and required response sections.
- \`chains.py\` assembles the runnable pipeline and exposes \`build_concept_explainer_chain()\`.
- \`cli.py\` provides a small command-line interface and invokes the chain.
- \`tests/\` checks the prompt template and the chain wiring. The chain test uses a fake \`Runnable\`, so it does not need to call a real model.

## Composition

\`\`\`python
chain = prompt | model | parser
result = chain.invoke({
    "concept": "Circuit Breaker Pattern",
    "audience": "Java microservices developer",
    "detail_level": "Intermediate",
})
\`\`\`

The pipe operator composes compatible LangChain Runnable components: the prompt output feeds the model, and the model response feeds the parser.

## Important boundaries

This project demonstrates orchestration, not factual verification. It does not have retrieval, chat history, memory, tool execution, source citations, or an evaluation dataset. The generated explanation can be wrong and should not be treated as authoritative without checking reliable sources.
