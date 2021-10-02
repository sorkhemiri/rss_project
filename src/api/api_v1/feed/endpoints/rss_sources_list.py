from fastapi import APIRouter
from starlette.requests import Request

from usecase.feed.implementation import RSSSourcesListUseCase

router = APIRouter()


@router.get("/sources/", tags=["sources-list", "feed"])
def rss_sources_list(request: Request):
    use_case = RSSSourcesListUseCase()
    return use_case.execute(request_model={})
