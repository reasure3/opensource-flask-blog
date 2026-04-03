import pytest
from flask import Flask

from client_validation import NoteFormSpec
from notes.note_controller import NoteController
from notes.note_models import Note
from notes.note_service import NoteService


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    service = NoteService(
        initial_notes=[
            Note(id=1, title="First note", content="First content"),
            Note(id=2, title="Second note", content="Second content"),
        ]
    )
    form_spec = NoteFormSpec()
    controller = NoteController(service, form_spec)
    controller.register_routes(app)
    return app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def test_get_notes_returns_200_and_notes_list_json(client) -> None:
    response = client.get("/notes")

    assert response.status_code == 200
    assert response.is_json
    payload = response.get_json()
    assert isinstance(payload, list)
    assert payload[0]["id"] == 1
    assert payload[0]["title"] == "First note"
    assert payload[0]["content"] == "First content"


def test_get_note_detail_returns_200_and_note_json_when_note_exists(client) -> None:
    response = client.get("/notes/1")

    assert response.status_code == 200
    assert response.is_json
    payload = response.get_json()
    assert payload["id"] == 1
    assert payload["title"] == "First note"
    assert payload["content"] == "First content"


def test_get_note_detail_returns_404_and_error_json_when_note_does_not_exist(client) -> None:
    response = client.get("/notes/999")

    assert response.status_code == 404
    assert response.is_json
    payload = response.get_json()
    assert "error" in payload or "message" in payload


def test_create_note_returns_201_and_created_note_json_for_valid_input(client) -> None:
    response = client.post(
        "/api/notes",
        json={
            "title": "New note",
            "content": "New content",
        },
    )

    assert response.status_code == 201
    assert response.is_json
    payload = response.get_json()
    assert isinstance(payload["id"], int)
    assert payload["title"] == "New note"
    assert payload["content"] == "New content"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": None, "content": "Valid content"},
        {"title": "", "content": "Valid content"},
        {"title": "   ", "content": "Valid content"},
        {"title": "a" * 51, "content": "Valid content"},
        {"title": "Valid title", "content": None},
        {"title": "Valid title", "content": ""},
        {"title": "Valid title", "content": "   "},
        {"title": "Valid title", "content": "a" * 201},
    ],
)
def test_create_note_returns_400_and_errors_json_for_invalid_input(client, payload) -> None:
    response = client.post("/api/notes", json=payload)

    assert response.status_code == 400
    assert response.is_json
    body = response.get_json()
    assert "errors" in body


def test_show_write_page_returns_200(client) -> None:
    response = client.get("/write")

    assert response.status_code == 200
    assert response.data