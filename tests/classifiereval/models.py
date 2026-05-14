import json
from pathlib import Path
from pydantic import BaseModel, Field

CLASSIFIER_TEST_FILE = str(Path(__file__).parent / "classifier_tests.jsonl")


class ClassifierTestQuestion(BaseModel):
    """Test question for classifier routing and prompt injection resistance."""
    input: str = Field(
        description="User query to classify.May include prompt injection text."
    )
    expected: str = Field(
        description="Expected routing label such as weather, filing, disaster, or general."
    )
    category: str = Field(
        description="Test category such as normal, ambiguous, prompt_injection or edge_case."
    )
    description: str = Field(
        description="description of what this test validates."
    )
    attack_type: str = Field(
        default=None,
        description="Injection subtype such as direct_override, roleplay, system_spoofing, tool_forcing."
    )   

class ClassifierEval(BaseModel):
    """Evalaution metrics for routing related tests"""
    question: str = Field(
        description="User query to classify.May include prompt injection text."
    )
    expected: str = Field(
        description="Excepted routing"
    )
    actual: str = Field(
        description="Actual routing received"
    )
    passed : bool = Field(
        description="Indicates whether testcase passed or not"
    )
    is_security_test: bool = Field(
        description="Whether this test validates security behavior such as prompt injection resistance, jailbreak prevention, or tool misuse protection."
    )


def load_classifier_tests() -> list[ClassifierTestQuestion]:
    """Load test questions from JSONL file."""
    tests = []
    with open(CLASSIFIER_TEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            tests.append(ClassifierTestQuestion(**data))
    return tests