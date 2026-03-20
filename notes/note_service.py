from typing import Optional

from .note_models import Note, NoteCreateRequest, ValidationResult

# 비즈니스 로직의 중심

# 이 기능이 비즈니스 규칙상 맞는지 판단하고 처리
# 예시
# 제목이 비어 있으면 invalid
# 내용이 너무 길면 invalid
# 유효하면 새 노트 생성
# 없는 id면 None 반환


class NoteService:
    """
    TADD Step 1용 서비스 레이어 계약.

    역할:
    - 노트 목록/상세 조회
    - 서버 측 입력 검증
    - 노트 생성
    """

    def __init__(
        self,
        initial_notes: Optional[list[Note]] = None,
        title_max_length: int = 50,
        content_max_length: int = 200,
    ) -> None:
        """
        Contract:
        - 초기 노트 목록을 주입받을 수 있다.
        - 서버/클라이언트가 공유할 길이 제한을 보관한다.
        - 지금 단계에서는 in-memory 저장소를 전제로 설계한다.
        """
        self._notes = initial_notes or []
        self._title_max_length = title_max_length
        self._content_max_length = content_max_length

    def list_notes(self) -> list[Note]:
        """
        Supporting Contract:
        - GET /notes 에서 사용할 전체 노트 목록 반환
        - 반환 타입은 list[Note]
        """
        raise NotImplementedError("RED stage: list_notes is not implemented yet.")

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """
        Spec 3:
        - note_id가 존재하면 해당 Note 반환
        - 존재하지 않으면 None 반환
        - 웹 레이어에서 None을 404로 매핑한다
        """
        raise NotImplementedError("RED stage: get_note_by_id is not implemented yet.")

    def validate_note_input(
        self,
        title: Optional[str],
        content: Optional[str],
    ) -> ValidationResult:
        """
        Spec 1:
        - title은 필수
        - content는 필수
        - 공백만 있는 입력은 허용하지 않음
        - title 최대 길이: 50
        - content 최대 길이: 200
        - 반환값은 ValidationResult
        """
        raise NotImplementedError("RED stage: validate_note_input is not implemented yet.")

    def create_note(self, request: NoteCreateRequest) -> Note:
        """
        Spec 2:
        - NoteCreateRequest를 받아 새 Note 생성
        - 생성 전 validate_note_input(...) 규칙을 만족해야 함
        - 성공 시 생성된 Note 반환
        - 실패 처리(400 응답 등)는 웹 레이어 테스트에서 다룬다
        """
        raise NotImplementedError("RED stage: create_note is not implemented yet.")