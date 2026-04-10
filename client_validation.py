"""노트 작성 폼과 공유하는 클라이언트 검증 규칙."""

from notes.note_models import (
    ClientValidationFieldRule,
    ClientValidationRules,
    DEFAULT_NOTE_CONTENT_MAX_LENGTH,
    DEFAULT_NOTE_TITLE_MAX_LENGTH,
    ErrorCode,
)

TITLE_FIELD_NAME = "title"
CONTENT_FIELD_NAME = "content"

CLIENT_VALIDATION_FIELD_DEFINITIONS = (
    {
        "field_name": TITLE_FIELD_NAME,
        "required": True,
        "required_error_code": ErrorCode.TITLE_REQUIRED,
        "too_long_error_code": ErrorCode.TITLE_TOO_LONG,
    },
    {
        "field_name": CONTENT_FIELD_NAME,
        "required": True,
        "required_error_code": ErrorCode.CONTENT_REQUIRED,
        "too_long_error_code": ErrorCode.CONTENT_TOO_LONG,
    },
)


class NoteFormSpec:
    """노트 도메인 규칙을 브라우저용 검증 정보로 제공한다."""

    def __init__(
        self,
        title_max_length: int = DEFAULT_NOTE_TITLE_MAX_LENGTH,
        content_max_length: int = DEFAULT_NOTE_CONTENT_MAX_LENGTH,
    ) -> None:
        """제목과 내용의 공통 길이 제한 값을 보관한다."""
        self.title_max_length = title_max_length
        self.content_max_length = content_max_length

    def get_rules(self) -> ClientValidationRules:
        """작성 폼에서 사용하는 전체 검증 규칙 객체를 반환한다."""
        return ClientValidationRules(
            title_required=True,
            content_required=True,
            title_max_length=self.title_max_length,
            content_max_length=self.content_max_length,
        )

    def get_error_messages(self) -> dict[ErrorCode, str]:
        """브라우저에서 표시할 사람이 읽기 쉬운 오류 메시지를 반환한다."""
        return {
            ErrorCode.TITLE_REQUIRED: "Title is required.",
            ErrorCode.CONTENT_REQUIRED: "Content is required.",
            ErrorCode.TITLE_TOO_LONG: f"Title must be at most {self.title_max_length} characters.",
            ErrorCode.CONTENT_TOO_LONG: f"Content must be at most {self.content_max_length} characters.",
        }

    def get_field_rules(self) -> list[ClientValidationFieldRule]:
        """클라이언트 JavaScript 검증에 사용할 필드별 규칙 객체를 반환한다."""
        max_length_by_field_name = {
            TITLE_FIELD_NAME: self.title_max_length,
            CONTENT_FIELD_NAME: self.content_max_length,
        }
        return [
            ClientValidationFieldRule(
                field_name=field_definition["field_name"],
                required=field_definition["required"],
                max_length=max_length_by_field_name[field_definition["field_name"]],
                required_error_code=field_definition["required_error_code"],
                too_long_error_code=field_definition["too_long_error_code"],
            )
            for field_definition in CLIENT_VALIDATION_FIELD_DEFINITIONS
        ]
