import pytest

from notes.note_models import ClientValidationRules
from client_validation import NoteFormSpec


def test_get_rules_returns_default_validation_rules_when_using_default_constructor() -> None:
    # Given
    spec = NoteFormSpec()

    # When
    rules = spec.get_rules()

    # Then
    assert isinstance(rules, ClientValidationRules)
    assert rules.title_required is True
    assert rules.content_required is True
    assert rules.title_max_length == 50
    assert rules.content_max_length == 200


def test_get_rules_reflects_custom_title_and_content_max_length() -> None:
    # Given
    spec = NoteFormSpec(title_max_length=80, content_max_length=300)

    # When
    rules = spec.get_rules()

    # Then
    assert rules.title_max_length == 80
    assert rules.content_max_length == 300


def test_get_error_messages_contains_required_and_too_long_message_keys() -> None:
    # Given
    spec = NoteFormSpec()

    # When
    messages = spec.get_error_messages()

    # Then
    assert isinstance(messages, dict)
    assert "title_required" in messages
    assert "content_required" in messages
    assert "title_too_long" in messages
    assert "content_too_long" in messages