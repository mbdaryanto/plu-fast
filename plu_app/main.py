from fastapi import FastAPI
from .version import get_version, get_program_name
from .routers import item

app = FastAPI(
    title="PLU App",
    description="Price Look Up Web Application",
    version=get_version(),
)

app.include_router(item.router)


@app.get('/')
async def index() -> str:
    return get_program_name()


@app.get('/info')
async def index() -> str:
    return get_program_name()
