# API

`GET /health` returns service status and version. `GET /ready` returns readiness.

`POST /v1/parse` accepts a multipart field named `file` containing a PDF and returns a partial canonical result. The initial implementation uses in-memory result storage.

```bash
curl -X POST http://localhost:8000/v1/parse -F file=@statement.pdf
```

`GET /v1/parses/{parse_id}` retrieves a result during the process lifetime. Errors use an `error.code`, safe message, and `retryable` flag.
