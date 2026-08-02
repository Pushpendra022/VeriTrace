import argparse
import json
from collections import Counter
from pathlib import Path

from app.evaluation.run_evaluation import VERDICTS, predict


def evaluate(path: Path, output: Path) -> dict[str, object]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) < 100:
        raise ValueError("Production-scale evaluation requires at least 100 independently labeled cases")
    required = {"case_id", "document_id", "source", "claim", "expected", "labeler_id"}
    if any(not required.issubset(row) or row["expected"] not in VERDICTS for row in rows):
        raise ValueError("Each JSONL row must contain valid case, document, source, claim, verdict, and labeler fields")
    predictions = [{**row, "predicted": predict(row["source"], row["claim"])} for row in rows]
    accuracy = sum(row["expected"] == row["predicted"] for row in predictions) / len(predictions)
    result = {"dataset": str(path), "cases": len(rows), "document_count": len({row["document_id"] for row in rows}), "labeler_count": len({row["labeler_id"] for row in rows}), "overall_accuracy": round(accuracy, 4), "confusion": dict(Counter(f"{row['expected']}->{row['predicted']}" for row in predictions)), "cases_with_predictions": predictions}
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate VeriTrace against independently human-labeled JSONL cases")
    parser.add_argument("dataset", type=Path); parser.add_argument("--output", type=Path, default=Path("app/evaluation/external_results.json"))
    args = parser.parse_args(); print(json.dumps(evaluate(args.dataset, args.output), indent=2))


if __name__ == "__main__": main()

