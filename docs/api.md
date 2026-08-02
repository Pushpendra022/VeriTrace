# API

All endpoints use the `/api` prefix.

- `GET /health` — database and provider status.
- `POST /documents` — multipart field `file`; PDF, TXT, or MD up to 20 MB.
- `GET /documents/{id}` and `GET /documents/{id}/pages` — metadata and extracted pages.
- `DELETE /documents/{id}` — cascade-delete a review.
- `POST /documents/{id}/claims`, `GET /documents/{id}/claims`, `POST /documents/{id}/claims/extract` — create, list, and extract claims.
- `PATCH /claims/{id}` and `DELETE /claims/{id}` — edit and remove claims.
- `POST /claims/{id}/verify` — retrieve, verify, validate, and persist a trace.
- `POST /documents/{id}/verify` — verify up to 15 claims with concurrency limited to two by default.
- `GET /verifications/{id}` — retrieve one structured trace.
- `GET /reviews` and `GET /reviews/{document_id}` — summaries and complete persisted review state.
- `POST /samples/{supported|contradicted|not-found|needs-review}/load` — load deterministic demonstrations.

Errors use `{ "error": { "code": "...", "message": "...", "details": {} } }`.

