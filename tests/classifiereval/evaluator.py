
from orchestration.graph_runner import run_query
from tests.classifiereval.models import ClassifierTestQuestion,load_classifier_tests,ClassifierEval
from orchestration.router import classify_message
from langchain_core.messages import HumanMessage

def evaluate_classifier_all():
    """Evaluate all classifier routing to tests using batched async execution."""
    tests = load_classifier_tests()
    total_tests = len(tests)
    for index, test in enumerate(tests):
        result = classifer_evaluation(test)
        progress = (index + 1) / total_tests
        yield test, result, progress

def classifer_evaluation(test: ClassifierTestQuestion) -> ClassifierEval:
    """Run classifier evaluation for given test question"""

    state = {
        "messages": [
            HumanMessage(content=test.input)
        ]
    }
    result = classify_message(state) 
    actual = result["route"]

    #run_query(test.input)
    is_security_test = False
    is_passed = False
    if test.category != "normal":
        is_security_test = True

    if test.expected == actual:
        is_passed = True
    
    evaluation = ClassifierEval(
        question=test.input,
        expected=test.expected,
        actual=actual,
        passed=is_passed,
        is_security_test=is_security_test
    )
    
    return evaluation



