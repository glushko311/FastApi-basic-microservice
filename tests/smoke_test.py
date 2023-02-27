import pytest
from httpx import AsyncClient
from sqlalchemy import insert, delete

from src.auth.models import Role, User
from .conftest import async_session_maker


@pytest.fixture(scope='function')
async def load_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=2, name="user", permissions=None)
        await session.execute(stmt)
        await session.commit()
    print('\nthis part will work before every test')
    yield None
    async with async_session_maker() as session:
        await session.execute(delete(User))
        await session.execute(delete(Role))
        await session.commit()
    print('\nthis part will work after every test')

class TestBaseSuite:
    async def test_smoke(self, ac: AsyncClient):
        response = await ac.get("/smoke")
        assert response.status_code == 200


class TestUserSuite:
    async def test_create_user(self, ac: AsyncClient, load_role):
        response = await ac.post("/user", json={
            "username": "john",
            "password": "john123",
            "email": "string@john.ee",
            "full_name": "John Doe"
            }
        )
        print(response.text)
        assert response.status_code == 200


# async def test_add_specific_operations(ac: AsyncClient):
#     response = await ac.post("/operations", json={
#         "id": 1,
#         "quantity": "25.5",
#         "figi": "figi_CODE",
#         "instrument_type": "bond",
#         "date": "2023-02-01T00:00:00",
#         "type": "Выплата купонов",
#     })
#
#     assert response.status_code == 200

# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/operations", params={
#         "operation_type": "Выплата купонов",
#     })
#
#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
#     assert len(response.json()["data"]) == 1