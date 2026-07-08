from langchain_core.output_parsers import PydanticOutputParser

from models import CodeReview

parser = PydanticOutputParser(
    pydantic_object=CodeReview
)