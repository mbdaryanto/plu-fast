from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .version import get_version, get_program_name
from .routers import item, graphql


app = FastAPI(
    title="PLU App",
    description="Price Look Up Web Application",
    version=get_version(),
)

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
async def index() -> str:
    return get_program_name()


@app.get('/info')
async def index() -> str:
    return get_program_name()
