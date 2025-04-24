import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import FastAPI

# project imports
from mars.service.agent import get_agent
from mars.web import router

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_chat(monkeypatch):
    class MockAgent:
        def run_query(self, query):
            return 'mocked response'

    agent = get_agent('mock', 'http://test')
    monkeypatch.setattr("mars.service.agent.LMAgentService", lambda name, url: MockService())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(f'/api/chat?lm_name=mock', json={"query": "test query"})

    assert response.status_code == 200
    assert response.json() == {"response": "mocked response"}

