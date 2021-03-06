from typing import Union, Dict, Any
import pathlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .version import get_version, get_program_name
from .routers import item, graphql
from .settings import is_dev_mode

fast_api_kwargs: Dict[str, Any] = {}

if not is_dev_mode():
    # disable /docs and /redoc if not in development mode
    fast_api_kwargs.update(
        docs_url=None,
        redoc_url=None,
    )

app = FastAPI(
    title="PLU App",
    description="Price Look Up Web Application",
    version=get_version(),
    **fast_api_kwargs,
)

# mount public static assets
public_path = pathlib.Path(__file__).parent / 'public'
assets_path = public_path / 'assets'
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

app.include_router(item.router)
app.include_router(graphql.router, prefix="/graphql")

origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://studio.apollographql.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index() -> Union[FileResponse, str]:
    index_path = public_path / 'index.html'
    if index_path.exists():
        return FileResponse(index_path)
    return get_program_name()


@app.get('/info')
async def info() -> str:
    return get_program_name()
