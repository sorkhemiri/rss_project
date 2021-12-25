from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import CreateRSSSourceUseCase
from validators.feed import CreateRSSSourceValidator

router = APIRouter()


class RequestData(BaseModel):
    key: str
    title: str
    description: Optional[str]
    link: str


@router.post("/source/create/", tags=["user_register", "auth"])
def create_rss_source(request: Request, request_data: RequestData):
    request_data = request_data.dict()
    use_case = CreateRSSSourceUseCase(validator=CreateRSSSourceValidator,
                                      rss_source_repository=RSSSourceRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
