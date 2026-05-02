from fastapi import APIRouter, Depends

from app.api.deps import get_event_repository, get_fingerprint_service
from app.schemas.ingest import IngestEventRequest, IngestEventResponse
from application.use_cases.ingest_event_use_case import IngestEventUseCase

ingest_router = APIRouter()


@ingest_router.post("/ingest", response_model=IngestEventResponse, status_code=201)
def ingest_event(
    request: IngestEventRequest,
    repository=Depends(get_event_repository),
    fingerprint_service=Depends(get_fingerprint_service),
) -> IngestEventResponse:
    use_case = IngestEventUseCase(repository, fingerprint_service)
    return use_case.execute(request)