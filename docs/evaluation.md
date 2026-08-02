# Evaluation

The checked-in dataset contains 22 synthetic, explicitly labeled financial/business evidence cases covering exact matches, paraphrases, numeric, percentage, date, currency, unit, entity and duration mismatches, absent facts, partial support, negation, approximation, ambiguity, multiple facts, and negative values.

Run from `backend`:

```bash
python -m app.evaluation.run_evaluation
```

The script exercises the local deterministic verdict baseline and writes every prediction plus measured aggregate metrics to `app/evaluation/results.json`. It does not call Gemini, fabricate model performance, or claim production accuracy. Results below must be updated only from an actual run.

<!-- EVALUATION_RESULTS -->

Actual run on 1 August 2026:

- Cases: 22; correct: 17; overall verdict accuracy: 77.27%.
- Precision — supported: 75.00%; contradicted: 77.78%; not found: 75.00%; needs review: 100.00%.
- Numeric mismatch detection: 75.00%.
- Quote verification and JSON validation fixture rates: 100.00%.

These figures are the direct output stored in `backend/app/evaluation/results.json`; they apply only to this deterministic synthetic evaluation.

Limitations: the dataset is small and synthetic, entity and unit reasoning is deliberately conservative, and the local evaluator measures deterministic guardrails rather than Gemini semantic quality. A production assessment needs independently authored documents and blinded human labels.

## Independent production evaluation

`python -m app.evaluation.run_external_evaluation LABELS.jsonl` accepts independently prepared data only when it contains at least 100 cases, document IDs, and labeler IDs. Required JSONL fields are `case_id`, `document_id`, `source`, `claim`, `expected`, and `labeler_id`. Human reviewers should label without seeing predictions, resolve disagreements before export, avoid documents used during development, and remove confidential material. No external dataset is bundled because manufacturing human labels would invalidate the evaluation.
