from langchain_core.prompts import ChatPromptTemplate

from parser import parser


review_prompt = ChatPromptTemplate.from_template(
"""
You are a Senior Software Engineer and Code Reviewer.

Analyze the following {language} code.

Your task is to perform a professional code review.

Return ONLY valid JSON. Do not include any commentary, markdown fences,
or text outside the JSON object.

{format_instructions}

Review the code for:

1. Bugs
2. Security vulnerabilities
3. Performance issues
4. Readability improvements
5. Best practices
6. Time complexity
7. Overall code quality score (0-100)
8. Short summary
9. Fully refactored code
10. Documentation / Docstrings

Code:

```{language}
{code}
```
"""
).partial(
    format_instructions=parser.get_format_instructions()
)