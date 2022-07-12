from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from ..db import get_session
from ..graphql.schema import schema


async def get_context(
    session = Depends(get_session),
):
    """
    Injecting orm session object into the context
    """
    return {
        'session': session
    }


router = GraphQLRouter(
    schema,
    context_getter=get_context,
)
