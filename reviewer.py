from agent import llm
from prompts import review_prompt
from parser import parser
from static_check import run_static_checks


review_chain = review_prompt | llm | parser


def review_code(code: str, language: str):
    """
    Runs the AI Code Review pipeline.

    Combines the LLM-generated review with deterministic static-analysis
    checks (e.g. pyflakes for Python), so mechanical issues like typos
    or undefined names are always caught even if the LLM misses them.

    Args:
        code: The source code to review.
        language: The programming language of the code.

    Returns:
        CodeReview Pydantic object
    """

    result = review_chain.invoke(
        {
            "code": code,
            "language": language
        }
    )

    static_bugs = run_static_checks(code, language)
    if static_bugs:
        # Merge and de-duplicate while preserving order
        result.bugs = list(dict.fromkeys(static_bugs + result.bugs))

    return result