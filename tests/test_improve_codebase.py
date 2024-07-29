import json
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app 
from app.models.request_and_response import ImproveCodebaseRequestBody
from app.models.analytic_event import ImproveCodebaseEvent

client = TestClient(app)

@pytest.fixture
def mock_gpt_service():
    with patch('app.services.dependencies.get_gpt_service') as mock:
        yield mock

@pytest.fixture
def mock_git_repo():
    with patch('app.api.endpoints.improve_codebase.GitRepo') as mock:
        yield mock

@pytest.fixture
def mock_event_logger():
    with patch('app.services.dependencies.get_event_logger') as mock:
        yield mock


def test_improve_codebase_success(mock_gpt_service, mock_git_repo, mock_event_logger):
    # Mock GPTService methods
    mock_gpt_service_instance = MagicMock()
    mock_gpt_service_instance.suggest_code_improvements.return_value = json.dumps({"changes": "mocked_changes"})
    mock_gpt_service_instance.reflect_on_diff.return_value = json.dumps({"corrections": []})
    mock_gpt_service.return_value = mock_gpt_service_instance

    # Mock GitRepo methods
    mock_git_repo_instance = MagicMock()
    mock_git_repo_instance.setup_local_repo.return_value = None
    mock_git_repo_instance.get_repo_contents.return_value = "mocked_repo_contents"
    mock_git_repo_instance.get_git_diff.return_value = "mocked_diff"
    mock_git_repo.return_value = mock_git_repo_instance


    # Mock EventLogger method
    mock_event_logger_instance = MagicMock()
    mock_event_logger_instance.log_event.return_value = None
    mock_event_logger.return_value = mock_event_logger_instance

    request_body = {
        "repoUrl": "https://github.com/example/repo",
        "prompt": "Improve the codebase"
    }

    response = client.post("/improve-codebase/", json=request_body)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"suggested_git_diff": "mocked_diff"}
