from fastapi import APIRouter
from starlette.requests import Request

from usecase.account.implementation import RSSSourcesList

router = APIRouter()


@router.get("/sources/", tags=["sources-list", "feed"])
def rss_sources_list(request: Request):
    use_case = RSSSourcesList()
    return use_case.execute(request_model={})
