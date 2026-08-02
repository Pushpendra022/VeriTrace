# Product decisions

- Four verdicts preserve uncertainty instead of forcing weak evidence into supported, contradicted, or absent.
- Exact quotes are mandatory for auditable positive or contradictory conclusions.
- Structured JSON is validated because model output is untrusted input.
- Gemini sits behind an adapter so business logic and tests are provider-independent.
- Deterministic number, percentage, date, and currency checks supplement semantic interpretation.
- Uploaded originals are deleted because extracted page text is sufficient for version-one review and avoids durable file-storage risk.
- Confidence is informational and combines retrieval, quote, deterministic, completeness, and model signals.
- Page-aware chunks reduce cost and distraction; 600-word targets with 75-word overlap preserve local context without sending whole documents.

