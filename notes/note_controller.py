from typing import Any

from flask import Flask, Response, jsonify, render_template_string, request

from client_validation import NoteFormSpec
from .note_models import NoteCreateRequest
from .note_service import NoteService

# 웹 레이어(HTTP 인터페이스)


class NoteController:
    """
    웹 레이어 계약 클래스.

    역할:
    - Flask route 등록
    - HTTP 요청/응답 형식 정의
    - 서비스 결과를 상태 코드와 JSON/페이지 응답으로 매핑
    """

    def __init__(self, note_service: NoteService, form_spec: NoteFormSpec) -> None:
        """
        Contract:
        - 비즈니스 로직은 NoteService에 위임
        - 클라이언트 검증 규칙은 NoteFormSpec에서 가져옴
        """
        self.note_service = note_service
        self.form_spec = form_spec

    def register_routes(self, app: Flask) -> None:
        """
        Contract:
        아래 public route를 Flask app에 등록한다.

        Routes:
        - GET /notes
        - GET /notes/<int:note_id>
        - GET /write
        - POST /api/notes
        """

        @app.get("/notes")
        def list_notes_route():
            return self.list_notes()

        @app.get("/notes/<int:note_id>")
        def get_note_detail_route(note_id: int):
            return self.get_note_detail(note_id)

        @app.get("/write")
        def show_write_page_route():
            return self.show_write_page()

        @app.post("/api/notes")
        def create_note_route():
            return self.create_note()

    def list_notes(self) -> tuple[Response, int]:
        """
        Supporting Contract:
        - GET /notes
        - 200 OK
        - 노트 목록 JSON 반환
        """
        return jsonify(
            [
                note.to_dict()
                for note in self.note_service.list_notes()
            ]
        ), 200

    def get_note_detail(self, note_id: int) -> tuple[Response, int]:
        """
        Spec 3:
        - 존재하는 note_id -> 200 + note JSON
        - 존재하지 않는 note_id -> 404 + error JSON
        """
        note = self.note_service.get_note_by_id(note_id)
        if note is None:
            return jsonify({"error": "Note not found"}), 404
        return jsonify(note.to_dict()), 200

    def show_write_page(self) -> str:
        """
        Spec 4:
        - GET /write
        - 노트 작성 페이지를 반환
        - 페이지에는 client-side validation 규칙이 주입되어야 함
        """
        rules = self.form_spec.get_rules()
        error_messages = self.form_spec.get_error_messages()
        return render_template_string(
            """
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8" />
                <title>Write Note</title>
              </head>
              <body>
                <h1>Write Note</h1>

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
                  const errorMessages = {{ error_messages | tojson }};
                  const form = document.getElementById("note-form");
                  const titleInput = document.getElementById("title");
                  const contentInput = document.getElementById("content");
                  const messageBox = document.getElementById("message");

                  function showMessage(text, isError) {
                    messageBox.textContent = text;
                    messageBox.style.color = isError ? "red" : "green";
                  }

                  function validateInput() {
                    const title = titleInput.value;
                    const content = contentInput.value;
                    const trimmedTitle = title.trim();
                    const trimmedContent = content.trim();

                    if (validationRules.title_required && (!trimmedTitle || trimmedTitle.length === 0)) {
                      return errorMessages.title_required;
                    }

                    if (trimmedTitle.length > validationRules.title_max_length) {
                      return errorMessages.title_too_long;
                    }

                    if (validationRules.content_required && (!trimmedContent || trimmedContent.length === 0)) {
                      return errorMessages.content_required;
                    }

                    if (trimmedContent.length > validationRules.content_max_length) {
                      return errorMessages.content_too_long;
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
            """,
            rules=rules.__dict__,
            error_messages=error_messages,
        )

    def create_note(self) -> tuple[Response, int]:
        """
        Spec 2:
        - POST /api/notes
        - request JSON: { "title": ..., "content": ... }
        - 유효한 입력 -> 201 + 생성된 note JSON
        - 유효하지 않은 입력 -> 400 + errors JSON
        """
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")
        content = payload.get("content")

        validation_result = self.note_service.validate_note_input(title, content)
        if not validation_result.is_valid:
            return jsonify({"errors": [error.value for error in validation_result.errors]}), 400

        note = self.note_service.create_note(NoteCreateRequest(title=title, content=content))
        return jsonify(note.to_dict()), 201
