from orchestration.graph_runner import run_query
from tests.responseeval.models import ResponseTestQuestion,ResponseEval,load_response_tests
from utils.models import judge_llm,get_judge_llm_model
def get_judge_llm_system_prompt() -> str:
    system_prompt = """
    You are an expert evaluator for LLM responses.

    Evaluate whether the actual response correctly and completely answers the user question compared to the expected answer.

    You will receive:
        1. User question
        2. Expected answer or expected behavior
        3. Actual LLM response

    Scoring:
        - correctness_score (1-5)
        5 = fully correct
        4 = mostly correct with minor issues
        3 = partially correct
        2 = mostly incorrect
        1 = incorrect or irrelevant

        - completeness_score (1-5)
        5 = fully answers the request
        4 = mostly complete with small omissions
        3 = partially complete
        2 = major details missing
        1 = barely answers the question

        Pass criteria:
        - passed = true only if correctness_score >= 4 and completeness_score >= 4

        Feedback:
        - Provide brief feedback explaining why the response passed or failed.

        Return only valid JSON matching this schema:

            {
            "question": "string",
            "expected_answer": "string",
            "actual_answer": "string",
            "passed": true,
            "correctness_score": 1,
            "completeness_score": 1,
            "feedback": "string"
            }

        Do not include markdown, explanations, or extra text outside JSON.

        Return ONLY JSON matching ResponseEval schema.
        No reasoning.
        No markdown.
        No code fences.
        No <think> tags.
        No text before or after JSON.

    """

    return system_prompt

def get_judge_llm_user_prompt(test: ResponseTestQuestion,generated_answer) -> str:
    judge_user_prompt=f"""Question:
            {test.question}

            Model Response:
            {generated_answer}

            Expected Answer:
            {test.expected_answer}

        """    

    
    return judge_user_prompt


def evaluate_response_all():
    """Evaluate all responses (answers) retrieved from LLM."""
    tests = load_response_tests()
    total_tests = len(tests)
    for index, test in enumerate(tests):
        result = response_evaluation(test)
        progress = (index + 1) / total_tests
        yield test, result, progress

def response_evaluation(test: ResponseTestQuestion) -> ResponseEval:
    """Run answer evaluation for given test question"""
    answer = run_query(test.question)


    judge_messages = [
        {
            "role": "system",
            "content": get_judge_llm_system_prompt()
        },
        {
            "role": "user",
            "content": get_judge_llm_user_prompt(test,answer)},
    ]

    judge_llm_response = judge_llm.chat.completions.parse(
            model=get_judge_llm_model(),
            messages=judge_messages,
            response_format=ResponseEval)


    evaluation = ResponseEval.model_validate_json(judge_llm_response.choices[0].message.content)
    
    return evaluation
