from settings import env_config
from fastapi import FastAPI
from router import main_router
from starlette.middleware.cors import CORSMiddleware
import http.cookies


http.cookies._is_legal_key = lambda _: True

app = FastAPI(title=env_config.app_title)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(main_router)


if env_config.debug and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000, debug=True)
