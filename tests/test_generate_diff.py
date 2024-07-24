from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_diff():
    response = client.post("/generate-diff", json={"repoUrl": "https://github.com/user/repo", "prompt": "convert it to Typescript"})
    assert response.status_code == 200
    assert "diff" in response.json()
