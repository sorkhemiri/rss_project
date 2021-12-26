from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import RSSSourceListUseCase
from validators.feed import RSSSourceListValidator

router = APIRouter()


@router.get("/sources/", tags=["sources-list", "feed"])
def rss_sources_list(request: Request, offset: int = 0, limit: int = 10):
    request_data = {"limit": limit, "offset": offset}
    use_case = RSSSourceListUseCase(validator=RSSSourceListValidator,
                                    rss_source_repository=RSSSourceRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
