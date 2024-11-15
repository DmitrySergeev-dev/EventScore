import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.api_v1 import dependencies
from src.core.config import settings
from src.entrypoints.app import app
from src.service_layer.unit_of_work import PostgresUnitOfWork


@pytest.fixture
def client(db_url):
    def override_uow():
        return PostgresUnitOfWork(url=db_url, echo=True)

    app.dependency_overrides[dependencies.db_uow] = override_uow
    client = TestClient(app=app, base_url="http://0.0.0.0:5555")
    return client


@pytest.fixture
def news_api_url(client):
    return f'{str(client.base_url)}{settings.api.prefix}' \
           f'{settings.api.v1.prefix}{settings.api.v1.news}/'


@pytest.mark.asyncio
class TestNewsAPI:

    async def test_get_news_list(self, client, news_api_url):
        response = client.get(url=news_api_url)
        assert response.status_code == status.HTTP_200_OK
