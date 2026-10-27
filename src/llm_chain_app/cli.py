import argparse

from .chains import build_concept_explainer_chain


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explain a technology concept using a LangChain pipeline.")
    parser.add_argument("--concept", required=True, help="The concept to explain.")
    parser.add_argument("--audience", default="software developer", help="Who the explanation is for.")
    parser.add_argument(
        "--detail-level",
        default="Intermediate",
        help="Depth of the explanation, such as Beginner or Intermediate.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chain = build_concept_explainer_chain()
    result = chain.invoke(
        {
            "concept": args.concept,
            "audience": args.audience,
            "detail_level": args.detail_level,
        }
    )
    print(result)


if __name__ == "__main__":
    main()
