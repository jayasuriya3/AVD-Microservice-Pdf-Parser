# API

`GET /health` returns service status and version. `GET /ready` returns readiness.

`POST /v1/parse` accepts a multipart field named `file` containing a PDF and returns a partial canonical result. For encrypted PDFs, include the optional multipart `password` field. The password is used only while processing the upload and is never returned or logged. The initial implementation uses in-memory result storage.

```bash
curl -X POST http://localhost:8000/v1/parse -F file=@statement.pdf
curl -X POST http://localhost:8000/v1/parse -F file=@protected-statement.pdf -F password='your-password'
```

`GET /v1/parses/{parse_id}` retrieves a result during the process lifetime. Errors use an `error.code`, safe message, and `retryable` flag.
