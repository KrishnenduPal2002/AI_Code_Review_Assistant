"""
Deterministic static-analysis checks that run alongside the LLM review.

LLMs can miss plain, mechanical bugs (typos, undefined names, unused
imports) in short snippets because they're reasoning about the code
rather than actually executing/parsing it. This module runs real static
analysis tools to catch that class of issue reliably, and the results
are merged into the LLM's findings.
"""

import io

from pyflakes.api import check
from pyflakes.reporter import Reporter


def python_static_bugs(code: str):
    """
    Run pyflakes against Python source and return a list of
    human-readable issue strings (undefined names, unused imports,
    unused variables, etc.).
    """
    out, err = io.StringIO(), io.StringIO()
    check(code, "submitted_code.py", Reporter(out, err))

    lines = []
    for stream in (out, err):
        for line in stream.getvalue().splitlines():
            line = line.strip()
            if line:
                # Strip the synthetic filename prefix for cleaner display
                lines.append(line.replace("submitted_code.py:", "line "))

    return lines


def run_static_checks(code: str, language: str):
    """
    Dispatch to the right static checker for the given language.
    Currently only Python is supported; other languages simply
    return an empty list (the LLM review still covers them).
    """
    if language.lower() == "python":
        return python_static_bugs(code)
    return []