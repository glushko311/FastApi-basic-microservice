from fastapi import APIRouter

from config import VERSION_PREFIX

smoke_router = APIRouter(
    prefix=VERSION_PREFIX,
    tags=['smoke']
)


@smoke_router.get("/smoke", response_model=dict)
async def smoke():
    return {'status': 'success'}

