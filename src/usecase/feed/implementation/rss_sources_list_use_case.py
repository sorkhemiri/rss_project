import json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from repositories.postgres import RSSSourceRepository
from usecase.interface import UseCaseInterface

from utils.exceptions import UseCaseException, status


class RSSSourcesListUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            rss_sources = RSSSourceRepository.get_list()
            rss_source_data = [item.dict(exclude_defaults=True) for item in rss_sources]
            return JSONResponse(content={"rss_sources": rss_source_data}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
