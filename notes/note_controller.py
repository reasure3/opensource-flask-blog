"""노트 관련 Flask 라우트를 담당하는 HTTP 컨트롤러 계층."""

from typing import Any

from flask import Flask, Response, jsonify, render_template_string, request

from client_validation import NoteFormSpec
from .note_models import NoteCreateRequest
from .note_service import NoteService

WRITE_NOTE_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Write Note</title>
  </head>
  <body>
    <h1>Write Note</h1>
    <p>브라우저에서 먼저 입력값을 검증한 뒤, in-memory 저장소에 노트를 생성합니다.</p>

    <form id="note-form">
      <div>
        <label for="title">Title</label>
        <input id="title" name="title" type="text" maxlength="{{ rules.title_max_length }}" />
      </div>

      <div>
        <label for="content">Content</label>
        <textarea id="content" name="content" maxlength="{{ rules.content_max_length }}"></textarea>
      </div>

      <button type="submit">Submit</button>
    </form>

    <div id="message"></div>

    <script>
      const validationRules = {{ rules | tojson }};
      const fieldRules = {{ field_rules | tojson }};
      const errorMessages = {{ error_messages | tojson }};
      const form = document.getElementById("note-form");
      const titleInput = document.getElementById("title");
      const contentInput = document.getElementById("content");
      const messageBox = document.getElementById("message");
      const inputByFieldName = {
        title: titleInput,
        content: contentInput
      };

      function showMessage(text, isError) {
        messageBox.textContent = text;
        messageBox.style.color = isError ? "red" : "green";
      }

      function validateInput() {
        for (const fieldRule of fieldRules) {
          const input = inputByFieldName[fieldRule.field_name];
          const value = input.value;
          const trimmedValue = value.trim();

          if (fieldRule.required && (!trimmedValue || trimmedValue.length === 0)) {
            return errorMessages[fieldRule.required_error_code];
          }

          if (trimmedValue.length > fieldRule.max_length) {
            return errorMessages[fieldRule.too_long_error_code];
          }
        }

        return null;
      }

      form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const validationError = validateInput();
        if (validationError) {
          showMessage(validationError, true);
          return;
        }

        try {
          const response = await fetch("/api/notes", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              title: titleInput.value,
              content: contentInput.value
            })
          });

          if (response.ok) {
            showMessage("Note saved!", false);
            titleInput.value = "";
            contentInput.value = "";
          } else {
            showMessage("Failed to save note.", true);
          }
        } catch (error) {
          showMessage("An error occurred.", true);
        }
      });
    </script>
  </body>
</html>
"""


class NoteController:
    """Flask HTTP 계층과 노트 서비스 계층을 연결한다."""

    def __init__(self, note_service: NoteService, form_spec: NoteFormSpec) -> None:
        """노트 서비스와 폼 명세 객체를 주입받아 보관한다."""
        self.note_service = note_service
        self.form_spec = form_spec

    def register_routes(self, app: Flask) -> None:
        """노트 관련 공개 라우트를 Flask 앱에 등록한다."""

        @app.get("/notes")
        def list_notes_route():
            """
            전체 노트 목록을 조회한다.
            ---
            tags:
              - 노트
            summary: 전체 노트 조회
            responses:
              200:
                description: 노트 목록을 JSON 배열로 반환
                content:
                  application/json:
                    schema:
                      type: array
                      items:
                        $ref: '#/components/schemas/Note'
            """
            return self.list_notes()

        @app.get("/notes/<int:note_id>")
        def get_note_detail_route(note_id: int):
            """
            ID로 특정 노트를 조회한다.
            ---
            tags:
              - 노트
            summary: 노트 상세 조회
            parameters:
              - in: path
                name: note_id
                required: true
                schema:
                  type: integer
                description: 조회할 노트의 숫자 ID
            responses:
              200:
                description: 요청한 노트 정보
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/Note'
              404:
                description: 해당 노트를 찾을 수 없음
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/ErrorResponse'
            """
            return self.get_note_detail(note_id)

        @app.get("/write")
        def show_write_page_route():
            """
            노트 작성 페이지를 렌더링한다.
            ---
            tags:
              - 노트
            summary: 노트 작성 페이지 조회
            responses:
              200:
                description: 클라이언트 검증 규칙이 포함된 HTML 폼 반환
                content:
                  text/html:
                    schema:
                      type: string
            """
            return self.show_write_page()

        @app.post("/api/notes")
        def create_note_route():
            """
            새 노트를 생성한다.
            ---
            tags:
              - 노트
            summary: JSON 입력으로 노트 생성
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/NoteCreateRequest'
            responses:
              201:
                description: 생성된 노트 반환
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/Note'
              400:
                description: 입력 검증 실패
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/ValidationErrorResponse'
            """
            return self.create_note()

    def list_notes(self) -> tuple[Response, int]:
        """전체 노트 컬렉션을 JSON 응답으로 반환한다."""
        return jsonify([note.to_dict() for note in self.note_service.list_notes()]), 200

    def get_note_detail(self, note_id: int) -> tuple[Response, int]:
        """노트가 존재하면 반환하고, 없으면 404 오류 JSON을 반환한다."""
        note = self.note_service.get_note_by_id(note_id)
        if note is None:
            return jsonify({"error": "Note not found"}), 404
        return jsonify(note.to_dict()), 200

    def show_write_page(self) -> str:
        """수동 노트 작성과 브라우저 검증에 사용하는 HTML 페이지를 렌더링한다."""
        return render_template_string(WRITE_NOTE_TEMPLATE, **self._get_write_page_context())

    def _get_write_page_context(self) -> dict[str, Any]:
        """작성 폼에 주입할 JSON 안전 형태의 검증 설정을 구성한다."""
        rules = self.form_spec.get_rules()
        return {
            "rules": rules.__dict__,
            "field_rules": [
                {
                    "field_name": field_rule.field_name,
                    "required": field_rule.required,
                    "max_length": field_rule.max_length,
                    "required_error_code": field_rule.required_error_code.value,
                    "too_long_error_code": field_rule.too_long_error_code.value,
                }
                for field_rule in self.form_spec.get_field_rules()
            ],
            "error_messages": {
                error_code.value: message
                for error_code, message in self.form_spec.get_error_messages().items()
            },
        }

    def create_note(self) -> tuple[Response, int]:
        """요청 JSON을 검증한 뒤 노트를 생성하고 실패 시 HTTP 400으로 변환한다."""
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")
        content = payload.get("content")

        validation_result = self.note_service.validate_note_input(title, content)
        if not validation_result.is_valid:
            return jsonify({"errors": [error.value for error in validation_result.errors]}), 400

        note = self.note_service.create_note(NoteCreateRequest(title=title, content=content))
        return jsonify(note.to_dict()), 201
