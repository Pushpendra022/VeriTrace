VERIFICATION_PROMPT = """You are a strict evidence-verification engine for financial and business documents.
Use only SOURCE CONTEXT. Do not infer unstated facts or invent quotes. Material numbers, percentages, dates, currencies, units, names, and timeframes must match.
Return JSON only with: verdict (SUPPORTED, CONTRADICTED, NOT_FOUND, NEEDS_REVIEW), confidence (0..1), quote (shortest exact source quote or empty), explanation (one sentence), page_number (integer or null), chunk_id (string or null).
CLAIM: {claim}\nSOURCE CONTEXT:\n{context}"""

CLAIM_EXTRACTION_PROMPT = """Extract independently verifiable factual financial or business claims from the document. Avoid opinions, marketing and predictions. Return JSON only: {{\"claims\":[{{\"claim_text\":str,\"category\":str,\"importance\":\"low\"|\"medium\"|\"high\"}}]}}. Maximum {limit}.\nDOCUMENT:\n{text}"""
