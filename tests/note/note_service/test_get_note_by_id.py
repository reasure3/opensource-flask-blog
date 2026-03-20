import pytest

from notes.note_models import Note
from notes.note_service import NoteService


@pytest.fixture
def service_with_notes() -> NoteService:
    return NoteService(
        initial_notes=[
            Note(id=1, title="First note", content="First content"),
            Note(id=2, title="Second note", content="Second content"),
        ]
    )


@pytest.fixture
def empty_service() -> NoteService:
    return NoteService(initial_notes=[])


def test_get_note_by_id_returns_matching_note_when_id_exists(service_with_notes: NoteService) -> None:
    # When
    result = service_with_notes.get_note_by_id(1)

    # Then
    assert result is not None
    assert result.id == 1
    assert result.title == "First note"
    assert result.content == "First content"


def test_get_note_by_id_returns_the_requested_note_among_multiple_notes(
    service_with_notes: NoteService,
) -> None:
    # When
    result = service_with_notes.get_note_by_id(2)

    # Then
    assert result is not None
    assert result.id == 2
    assert result.title == "Second note"
    assert result.content == "Second content"


def test_get_note_by_id_returns_none_when_note_id_does_not_exist(service_with_notes: NoteService) -> None:
    # When
    result = service_with_notes.get_note_by_id(999)

    # Then
    assert result is None


def test_get_note_by_id_returns_none_when_initial_note_list_is_empty(empty_service: NoteService) -> None:
    # When
    result = empty_service.get_note_by_id(1)

    # Then
    assert result is None