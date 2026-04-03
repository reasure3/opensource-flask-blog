from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

DEFAULT_NOTE_TITLE_MAX_LENGTH = 50
DEFAULT_NOTE_CONTENT_MAX_LENGTH = 200

# 데이터 구조를 정의하는 모듈


class ErrorCode(str, Enum):
    """
    Spec 1 / 2 / 3에서 공통으로 사용할 machine-readable 에러 코드.
    테스트에서는 문자열 비교보다 이 코드를 비교하는 쪽이 명확하다.
    """
    TITLE_REQUIRED = "TITLE_REQUIRED"
    TITLE_TOO_LONG = "TITLE_TOO_LONG"
    CONTENT_REQUIRED = "CONTENT_REQUIRED"
    CONTENT_TOO_LONG = "CONTENT_TOO_LONG"
    NOTE_NOT_FOUND = "NOTE_NOT_FOUND"


@dataclass
class ValidationResult:
    """
    Spec 1: validate_note_input(...)의 반환 DTO

    Contract:
    - is_valid: 모든 검증 규칙 통과 여부
    - errors: 실패한 규칙의 에러 코드 목록
    """
    is_valid: bool
    errors: list[ErrorCode] = field(default_factory=list)


@dataclass
class NoteCreateRequest:
    """
    Spec 2: POST /api/notes 요청 DTO

    Contract:
    - title: 사용자가 입력한 제목
    - content: 사용자가 입력한 본문
    """
    title: Optional[str]
    content: Optional[str]


@dataclass
class Note:
    """
    Spec 2 / 3: 생성 및 조회에 사용하는 엔티티

    Contract:
    - id: 노트 식별자
    - title: 노트 제목
    - content: 노트 내용
    """
    id: int
    title: str
    content: str

    def to_dict(self) -> dict[str, int | str]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
        }


@dataclass
class ClientValidationRules:
    """
    Spec 4: 클라이언트 측 검증 규칙 DTO

    Contract:
    - title/content는 필수
    - 최대 길이 제한 제공
    """
    title_required: bool = True
    content_required: bool = True
    title_max_length: int = DEFAULT_NOTE_TITLE_MAX_LENGTH
    content_max_length: int = DEFAULT_NOTE_CONTENT_MAX_LENGTH
