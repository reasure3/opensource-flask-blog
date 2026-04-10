"""노트 생성, 검증, 조회를 담당하는 비즈니스 로직."""

from typing import Optional

from .note_models import (
    DEFAULT_NOTE_CONTENT_MAX_LENGTH,
    DEFAULT_NOTE_TITLE_MAX_LENGTH,
    ErrorCode,
    Note,
    NoteCreateRequest,
    ValidationResult,
)


class NoteService:
    """in-memory 노트 저장소와 입력 검증 규칙을 제공한다."""

    def __init__(
        self,
        initial_notes: Optional[list[Note]] = None,
        title_max_length: int = DEFAULT_NOTE_TITLE_MAX_LENGTH,
        content_max_length: int = DEFAULT_NOTE_CONTENT_MAX_LENGTH,
    ) -> None:
        """초기 노트와 검증 설정을 받아 서비스를 초기화한다."""
        self._notes = list(initial_notes) if initial_notes is not None else []
        self._title_max_length = title_max_length
        self._content_max_length = content_max_length

    def list_notes(self) -> list[Note]:
        """전체 노트 목록의 복사본을 반환한다."""
        return list(self._notes)

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """ID에 해당하는 노트를 반환하고, 없으면 ``None`` 을 반환한다."""
        for note in self._notes:
            if note.id == note_id:
                return note
        return None

    def validate_note_input(
        self,
        title: Optional[str],
        content: Optional[str],
    ) -> ValidationResult:
        """필수 입력 여부와 길이 제한 규칙에 따라 노트 입력값을 검증한다."""
        errors: list[ErrorCode] = []

        if title is None or title.strip() == "":
            errors.append(ErrorCode.TITLE_REQUIRED)
        elif len(title) > self._title_max_length:
            errors.append(ErrorCode.TITLE_TOO_LONG)

        if content is None or content.strip() == "":
            errors.append(ErrorCode.CONTENT_REQUIRED)
        elif len(content) > self._content_max_length:
            errors.append(ErrorCode.CONTENT_TOO_LONG)

        return ValidationResult(is_valid=not errors, errors=errors)

    def create_note(self, request: NoteCreateRequest) -> Note:
        """검증이 통과한 요청으로 새 노트를 생성하고 저장한다."""
        validation_result = self.validate_note_input(request.title, request.content)
        if not validation_result.is_valid:
            raise ValueError("Invalid note input")

        next_id = max((note.id for note in self._notes), default=0) + 1
        note = Note(id=next_id, title=request.title, content=request.content)
        self._notes.append(note)
        return note
