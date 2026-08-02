# Security

Uploads are streamed into OS-generated temporary filenames, capped while streaming, validated by extension and MIME, parsed as data, and deleted in `finally`. User filenames are reduced to basenames and sanitized. Originals are never persisted. Empty, corrupt, scanned, invalid-encoding, oversized, and unsupported documents receive stable errors.

Pydantic validates API and model-provider data. Production CORS requires explicit origins. SlowAPI applies a basic IP limit, bulk work is capped and concurrency-controlled, and identical claim/context verification is cached. Secrets remain backend environment variables and are excluded by `.gitignore`. Logs never include API keys or document bodies.

There is intentionally no authentication. Public deployments should use conservative platform request limits and may periodically delete review rows older than seven days.

`REVIEW_RETENTION_DAYS` defaults to seven. At backend startup, reviews older than that threshold are deleted with their pages, chunks, claims, and verifications. Set a different positive duration where policy requires it.
