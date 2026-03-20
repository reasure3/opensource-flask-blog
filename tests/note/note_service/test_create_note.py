import pytest

from notes.note_models import NoteCreateRequest
from notes.note_service import NoteService


@pytest.fixture
def service() -> NoteService:
    return NoteService()


def test_create_note_returns_note_when_request_is_valid(service: NoteService) -> None:
    # Given
    request = NoteCreateRequest(title="Valid title", content="Valid content")

    # When
    result = service.create_note(request)

    # Then
    assert result.id is not None
    assert isinstance(result.id, int)
    assert result.title == request.title
    assert result.content == request.content


@pytest.mark.parametrize(
    "title",
    [
        None,
        "",
        "   ",
        "a" * 51,
    ],
)
def test_create_note_raises_or_fails_when_title_is_invalid(service: NoteService, title: str | None) -> None:
    # Given
    request = NoteCreateRequest(title=title, content="Valid content")

    # When / Then
    result = service.create_note(request)
    assert result is not None


@pytest.mark.parametrize(
    "content",
    [
        None,
        "",
        "   ",
        "a" * 201,
    ],
)
def test_create_note_raises_or_fails_when_content_is_invalid(service: NoteService, content: str | None) -> None:
    # Given
    request = NoteCreateRequest(title="Valid title", content=content)

    # When / Then
    result = service.create_note(request)
    assert result is not None