# test_app.py

import configparser
import io

import pytest
from manager import app as flask_app
from manager import forms


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_show_environments(monkeypatch, client):
    # Mock configparser to return fake environments
    def mock_read(filename):
        pass  # Do nothing

    def mock_sections():
        return ["dev", "prod"]

    def mock_getitem(self, key):
        return {"url": "http://example.com"} if key == "dev" else {"url": "http://prod.com"}

    configparser.ConfigParser.read = mock_read
    configparser.ConfigParser.sections = mock_sections
    configparser.ConfigParser.__getitem__ = mock_getitem

    response = client.get("/")
    assert response.status_code == 200
    assert b"environments" in response.data  # crude check: template renders


def test_request_runner_get(client):
    response = client.get("/request-runner")
    assert response.status_code == 200
    assert b"form" in response.data or b"Request" in response.data


def test_request_runner_post_valid(monkeypatch, client):
    class DummyForm:
        def validate_on_submit(self):
            return True

        @property
        def environment_name(self):
            return type("data", (), {"data": "dev"})

        @property
        def project_group(self):
            return type("data", (), {"data": "my-group"})

        @property
        def tags(self):
            return type("data", (), {"data": "tag1,tag2"})

    monkeypatch.setattr(forms, "RequestForm", lambda: DummyForm())

    response = client.post("/request-runner", data={})
    assert response.status_code == 302
    assert "/success" in response.headers["Location"]


def test_request_runner_post_invalid(monkeypatch, client):
    class DummyForm:
        def validate_on_submit(self):
            return False

    monkeypatch.setattr(forms, "RequestForm", lambda: DummyForm())

    response = client.post("/request-runner", data={})
    assert response.status_code == 200  # stays on form


def test_success(client):
    response = client.get("/success")
    assert response.status_code == 200
    assert b"GitLab Runner request submitted successfully" in response.data
