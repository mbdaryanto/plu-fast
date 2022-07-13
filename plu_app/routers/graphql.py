from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from ..settings import is_dev_mode
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
    graphiql=is_dev_mode(),
)
