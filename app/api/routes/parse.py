from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.api.dependencies import get_parse_service, get_repository
from app.application.parse_service import ParseService
from app.core.config import get_settings
from app.core.exceptions import CASParserError
from app.models.responses import ErrorDetail, ErrorResponse
from app.models.statement import Statement
from app.repositories.in_memory import InMemoryParseRepository

router = APIRouter(prefix="/v1", tags=["parsing"])


@router.post("/parse", response_model=Statement, responses={400: {"model": ErrorResponse}})
async def parse_pdf(
    file: UploadFile = File(...),
    password: str | None = Form(default=None),
    service: ParseService = Depends(get_parse_service),
    repository: InMemoryParseRepository = Depends(get_repository),
) -> Statement:
    settings = get_settings()
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail="Only PDF uploads are supported")
    payload = await file.read(settings.max_upload_size_bytes + 1)
    if len(payload) > settings.max_upload_size_bytes:
        raise HTTPException(status_code=413, detail="PDF exceeds configured size limit")
    if not payload.startswith(b"%PDF-"):
        raise HTTPException(status_code=415, detail="Uploaded file is not a PDF")
    parse_id = uuid4()
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(prefix="cas-", suffix=".pdf", delete=False) as temporary:
            temporary.write(payload)
            temporary_path = Path(temporary.name)
        result = service.parse_file(temporary_path, parse_id=parse_id, password=password)
        repository.save(result)
        return result
    except CASParserError as exc:
        raise HTTPException(status_code=400, detail=ErrorDetail(code=exc.code, message="Unable to parse document", retryable=exc.retryable).model_dump()) from exc
    finally:
        if temporary_path:
            temporary_path.unlink(missing_ok=True)


@router.get("/parses/{parse_id}", response_model=Statement)
def get_parse(parse_id: UUID, repository: InMemoryParseRepository = Depends(get_repository)) -> Statement:
    result = repository.get(parse_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parse result not found")
    return result
