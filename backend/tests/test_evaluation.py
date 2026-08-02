from app.evaluation.run_evaluation import predict


def test_evaluator_covers_core_verdicts() -> None:
    assert predict("Revenue was $11.4 million.", "Revenue was $11.4 million.") == "SUPPORTED"
    assert predict("Revenue was $11.4 million.", "Revenue was $14.2 million.") == "CONTRADICTED"
    assert predict("Revenue increased.", "The company has 340 customers.") == "NOT_FOUND"

