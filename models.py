from typing import List

from pydantic import BaseModel, Field


class CodeReview(BaseModel):
    """Structured output schema for an AI-generated code review."""

    bugs: List[str] = Field(
        default_factory=list,
        description="List of bugs or logical errors found in the code"
    )
    security_vulnerabilities: List[str] = Field(
        default_factory=list,
        description="List of security vulnerabilities found in the code"
    )
    performance_issues: List[str] = Field(
        default_factory=list,
        description="List of performance issues or inefficiencies found in the code"
    )
    readability_improvements: List[str] = Field(
        default_factory=list,
        description="Suggestions to improve code readability"
    )
    best_practices: List[str] = Field(
        default_factory=list,
        description="Best practice violations and recommendations"
    )
    time_complexity: str = Field(
        default="",
        description="Estimated time complexity of the code (Big-O notation)"
    )
    quality_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Overall code quality score from 0 to 100"
    )
    summary: str = Field(
        default="",
        description="A short summary (2-4 sentences) of the overall code review"
    )
    refactored_code: str = Field(
        default="",
        description="The fully refactored, corrected version of the code"
    )
    documentation: str = Field(
        default="",
        description="Documentation and docstrings explaining the refactored code"
    )