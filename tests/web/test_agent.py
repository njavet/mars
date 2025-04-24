import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import FastAPI

# project imports
from mars.domain.agent_factory import AgentFactory
from mars.web.agent import router

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_chat(monkeypatch):
    class MockService:
        def handle_query(self, query):
            return 'mocked response'

    class MockLM:
        def generate(self, prompt):
            return 'mocked response'

    agent_factory = AgentFactory()
    agent_factory.registry['mock'] = MockLM()
    monkeypatch.setattr("mars.service.agent.LMAgentService", lambda name, url: MockService())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(f'/api/chat?lm_name=mock', json={"query": "test query"})

    assert response.status_code == 200
    assert response.json() == {"response": "mocked response"}

