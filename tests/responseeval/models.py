import json
from pathlib import Path
from pydantic import BaseModel, Field

RESPONSE_TEST_FILE = str(Path(__file__).parent / "response_tests.jsonl")

class ResponseTestQuestion(BaseModel):
    """Test case for evaluating final LLM response quality."""

    question: str = Field(
        description="User question sent to the system."
    )

    expected_answer: str = Field(
        description="Reference answer or expected behavior."
    )

    description: str = Field(
        description="Description of what this test validates."
    )

    category: str = Field(
        description="Test type such as normal, edge_case, ambiguous."
    )

class ResponseEval(BaseModel):
    """Evaluation result for final LLM response."""

    question: str = Field(
        description="Original user question."
    )

    expected_answer: str = Field(
        description="Expected answer or behavior."
    )

    actual_answer: str = Field(
        description="Actual LLM response."
    )

    passed: bool = Field(
        description="Overall pass/fail."
    )

    correctness_score: int = Field(
        description="Score from 1-5 indicating factual correctness."
    )

    completeness_score: int = Field(
        description="Score from 1-5 indicating whether response fully answered the query."
    )

    feedback: str = Field(
        description="Brief explanation of why response passed or failed."
    )    



def load_response_tests() -> list[ResponseTestQuestion]:
    """Load test questions from JSONL file."""
    tests = []
    with open(RESPONSE_TEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            tests.append(ResponseTestQuestion(**data))
    return tests    