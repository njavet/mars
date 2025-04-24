from fastapi.testclient import TestClient
from mars.main import create_app
import requests

app = create_app()
client = TestClient(app)


def test_chat_route(mocker):
    mock_post = mocker.patch('mars.service.lm.requests.post')

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'response': 'mocked result'}

    payload = {
        "lm_name": "llama3",
        "base_url": "http://localhost:11434",
        "query": "Summarize diagnosis"
    }

    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    assert response.json() == {'response': 'mocked result'}

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs['json']['prompt'] == "Summarize diagnosis"
    assert kwargs['json']['model'] == "llama3"
