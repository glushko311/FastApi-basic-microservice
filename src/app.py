import typing

from fastapi import FastAPI, APIRouter

from src.auth.router import auth_router, user_router
from src.item.routers import (
    item_router, collection_router, tag_router
)
from src.smoke_router import smoke_router

app = FastAPI()

# Please register new router in this list
routers: typing.List[APIRouter] = [
    smoke_router,
    auth_router,
    user_router,
    item_router,
    collection_router,
    tag_router
]
for router in routers:
    app.include_router(router=router)
