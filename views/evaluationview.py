import streamlit as st
import pandas as pd
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv
from collections import Counter
from tests.classifiereval.evaluator import evaluate_classifier_all
from tests.responseeval.evaluator import evaluate_response_all

def render():
    st.title("📊 Evaluation")
    st.write("Evaluate Orchestration and Responses")

    st.markdown("---")

    st.markdown("### Classifier Evaluation")
    if st.button("▶ Run Classifier Evaluation", type="primary", key="classifier_evaluation", use_container_width=True):
        classifier_evaluation()

    st.divider()
    st.markdown("### Response Evaluation")
    if st.button("▶ Run Response Evaluation", type="primary", key="response_evaluation", use_container_width=True):
        response_evaluation()


def classifier_evaluation():
    count = 0
    results = []
    test_cases = []
    progress_bar = st.progress(0, text="Starting classifier evaluation…")
    #metrics_slot = st.empty()
    for test, result, prog_value in evaluate_classifier_all():
        count += 1
        eval_result = result
        test_cases.append(test)
        results.append(eval_result)
        progress_bar.progress(prog_value, text=f"Evaluating test {count}…")
    
    progress_bar.empty()
    overall_accuracy = sum(r.passed for r in results) / len(results) if results else 0

    security_results = [r for r in results if r.is_security_test]
    security_total = len(security_results)
    security_passed = sum(r.passed for r in security_results)
    security_failed = security_total - security_passed
    security_accuracy = security_passed / security_total

    with st.container():
        st.subheader("Overall Results")
        cols = st.columns(4)
        cols[0].metric("Total Tests", len(results))
        cols[1].metric("Passed", sum(r.passed for r in results))
        cols[2].metric("Failed", sum(not r.passed for r in results))
        cols[3].metric("Accuracy", f"{overall_accuracy:.2%}")

    with st.container():
        st.subheader("Security Test Results")
        cols = st.columns(4)
        cols[0].metric("Security Tests", security_total)
        cols[1].metric("Security Passed", security_passed)
        cols[2].metric("Security Failed", security_failed)
        cols[3].metric("Security Accuracy", f"{security_accuracy:.2%}")

    table_data = []

    for test, result in zip(test_cases, results):
        table_data.append({
            "Question": test.input,
            "Excepted": result.expected,
            "Actual": result.actual,
            "Passed": result.passed,
            "Evaluated for Security":result.is_security_test
        })
    df = pd.DataFrame(table_data)
    for i, row in df.iterrows():
        with st.expander(f"Result {i+1}"):
            for col in df.columns:
                st.write(f"**{col}:** {row[col]}")


def response_evaluation():
    count = 0
    results = []
    test_cases = []
    progress_bar = st.progress(0, text="Starting response evaluation…")
    for test, result, prog_value in evaluate_response_all():
        count += 1
        eval_result = result
        test_cases.append(test)
        results.append(eval_result)
        progress_bar.progress(prog_value, text=f"Evaluating test {count}…")
    
    progress_bar.empty()
    average_correctness = sum(r.correctness_score for r in results) / len(results) if results else 0
    average_completeness = sum(r.completeness_score for r in results) / len(results) if results else 0

    with st.container():
        st.subheader("Overall Results")
        cols = st.columns(5)
        cols[0].metric("Total Tests", len(results))
        cols[1].metric("Passed", sum(r.passed for r in results))
        cols[2].metric("Failed", sum(not r.passed for r in results))
        cols[3].metric("Correctness(1-5)", f"{average_correctness:.2f} / 5")
        cols[4].metric("Completeness(1-5)", f"{average_completeness:.2f} / 5")

    table_data = []

    for test, result in zip(test_cases, results):
        table_data.append({
            "Question": test.question,
            "Excepted": result.expected_answer,
            "Actual": result.actual_answer,
            "Passed": result.passed,
            "Correctness Score":result.correctness_score,
            "Completeness Score":result.completeness_score,
            "Feedback" : result.feedback
        })

    df = pd.DataFrame(table_data)
    for i, row in df.iterrows():
        with st.expander(f"Result {i+1}"):
            for col in df.columns:
                st.write(f"**{col}:** {row[col]}")