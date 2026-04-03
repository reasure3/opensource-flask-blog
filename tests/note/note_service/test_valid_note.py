import pytest

from notes.note_models import ErrorCode
from notes.note_service import NoteService


@pytest.fixture
def service() -> NoteService:
    return NoteService()


def test_validate_note_input_returns_valid_result_when_title_and_content_are_valid(service: NoteService) -> None:
    # Given
    title = "Valid title"
    content = "Valid content"

    # When
    result = service.validate_note_input(title, content)

    # Then
    assert result.is_valid is True
    assert result.errors == []


@pytest.mark.parametrize(
    "title, expected_error",
    [
        (None, ErrorCode.TITLE_REQUIRED),
        ("", ErrorCode.TITLE_REQUIRED),
        ("   ", ErrorCode.TITLE_REQUIRED),
    ],
)
def test_validate_note_input_returns_title_required_error_for_missing_or_blank_title(
    service: NoteService,
    title: str | None,
    expected_error: ErrorCode,
) -> None:
    # When
    result = service.validate_note_input(title, "Valid content")

    # Then
    assert result.is_valid is False
    assert result.errors == [expected_error]


def test_validate_note_input_returns_title_too_long_error_when_title_exceeds_max_length(service: NoteService) -> None:
    # Given
    title = "a" * 51
    content = "Valid content"

    # When
    result = service.validate_note_input(title, content)

    # Then
    assert result.is_valid is False
    assert result.errors == [ErrorCode.TITLE_TOO_LONG]


@pytest.mark.parametrize(
    "content, expected_error",
    [
        (None, ErrorCode.CONTENT_REQUIRED),
        ("", ErrorCode.CONTENT_REQUIRED),
        ("   ", ErrorCode.CONTENT_REQUIRED),
    ],
)
def test_validate_note_input_returns_content_required_error_for_missing_or_blank_content(
    service: NoteService,
    content: str | None,
    expected_error: ErrorCode,
) -> None:
    # When
    result = service.validate_note_input("Valid title", content)

    # Then
    assert result.is_valid is False
    assert result.errors == [expected_error]


def test_validate_note_input_returns_content_too_long_error_when_content_exceeds_max_length(service: NoteService) -> None:
    # Given
    title = "Valid title"
    content = "a" * 201

    # When
    result = service.validate_note_input(title, content)

    # Then
    assert result.is_valid is False
    assert result.errors == [ErrorCode.CONTENT_TOO_LONG]


def test_validate_note_input_returns_all_relevant_errors_when_both_fields_are_invalid(
    service: NoteService,
) -> None:
    # Given
    title = "a" * 51
    content = "a" * 201

    # When
    result = service.validate_note_input(title, content)

    # Then
    assert result.is_valid is False
    assert result.errors == [ErrorCode.TITLE_TOO_LONG, ErrorCode.CONTENT_TOO_LONG]