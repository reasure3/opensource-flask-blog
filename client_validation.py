from notes.note_models import ClientValidationRules


class NoteFormSpec:
    """
    Spec 4용 계약 클래스.

    목적:
    - 서버와 동일한 검증 규칙을 클라이언트(JS / 템플릿)에도 전달할 수 있게 한다.
    - 나중에 /write 페이지에서 이 규칙을 사용해 client-side verification을 구현한다.
    """

    def __init__(
        self,
        title_max_length: int = 50,
        content_max_length: int = 200,
    ) -> None:
        """
        Contract:
        - 클라이언트 검증 규칙의 기준값을 보관한다.
        """
        self.title_max_length = title_max_length
        self.content_max_length = content_max_length

    def get_rules(self) -> ClientValidationRules:
        """
        Spec 4:
        - 클라이언트가 사용할 검증 규칙 DTO 반환
        - title/content 필수 여부와 최대 길이를 포함
        """
        raise NotImplementedError("RED stage: get_rules is not implemented yet.")

    def get_error_messages(self) -> dict[str, str]:
        """
        Spec 4:
        - 클라이언트 화면에 보여줄 에러 메시지 집합 반환
        - 예: title required, content required, too long 등
        """
        raise NotImplementedError("RED stage: get_error_messages is not implemented yet.")