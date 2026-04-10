"""노트 애플리케이션에서 사용하는 도메인 모델과 DTO 모음."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

DEFAULT_NOTE_TITLE_MAX_LENGTH = 50
DEFAULT_NOTE_CONTENT_MAX_LENGTH = 200


class ErrorCode(str, Enum):
    """검증 및 조회 실패를 표현하는 기계 친화적 오류 코드."""

    TITLE_REQUIRED = "TITLE_REQUIRED"
    TITLE_TOO_LONG = "TITLE_TOO_LONG"
    CONTENT_REQUIRED = "CONTENT_REQUIRED"
    CONTENT_TOO_LONG = "CONTENT_TOO_LONG"
    NOTE_NOT_FOUND = "NOTE_NOT_FOUND"


@dataclass
class ValidationResult:
    """노트 입력 검증 성공 여부와 오류 목록을 표현한다."""

    is_valid: bool
    errors: list[ErrorCode] = field(default_factory=list)


@dataclass
class NoteCreateRequest:
    """노트 생성 시 사용하는 입력 DTO."""

    title: Optional[str]
    content: Optional[str]


@dataclass
class Note:
    """저장된 노트 엔티티."""

    id: int
    title: str
    content: str

    def to_dict(self) -> dict[str, int | str]:
        """노트를 JSON 직렬화 가능한 딕셔너리로 변환한다."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
        }


@dataclass
class ClientValidationRules:
    """브라우저 작성 폼과 공유하는 검증 규칙 묶음."""

    title_required: bool = True
    content_required: bool = True
    title_max_length: int = DEFAULT_NOTE_TITLE_MAX_LENGTH
    content_max_length: int = DEFAULT_NOTE_CONTENT_MAX_LENGTH


@dataclass
class ClientValidationFieldRule:
    """브라우저에 노출되는 필드 단위 검증 메타데이터."""

    field_name: str
    required: bool
    max_length: int
    required_error_code: ErrorCode
    too_long_error_code: ErrorCode
