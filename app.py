"""Flask Study Notes Service의 애플리케이션 진입점."""

from collections import OrderedDict

from flask import Flask, jsonify
from flasgger import Swagger

from client_validation import NoteFormSpec
from notes.note_controller import NoteController
from notes.note_models import Note
from notes.note_service import NoteService


def create_app() -> Flask:
    """Flask 애플리케이션 인스턴스를 생성하고 기본 구성을 적용한다."""
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SWAGGER"] = {
        "title": "Flask Study Notes Service API 문서",
        "uiversion": 3,
        "openapi": "3.0.2",
    }

    Swagger(
        app,
        template={
            "info": {
                "title": "Flask Study Notes Service API 문서",
                "version": "1.0.0",
                "description": (
                    "테스트, 문서화, Git 워크플로 연습을 위해 만든 "
                    "작은 Flask 노트 서비스입니다."
                ),
            },
            "components": {
                "schemas": {
                    "Note": {
                        "type": "object",
                        "required": ["id", "title", "content"],
                        "properties": OrderedDict(
                            [
                                ("id", {"type": "integer", "example": 1}),
                                ("title", {"type": "string", "example": "환영 노트"}),
                                (
                                    "content",
                                    {
                                        "type": "string",
                                        "example": "수동 테스트를 위해 제공되는 기본 노트입니다.",
                                    },
                                ),
                            ]
                        ),
                    },
                    "NoteCreateRequest": {
                        "type": "object",
                        "required": ["title", "content"],
                        "properties": OrderedDict(
                            [
                                (
                                    "title",
                                    {
                                        "type": "string",
                                        "maxLength": 50,
                                        "example": "스프린트 회고",
                                    },
                                ),
                                (
                                    "content",
                                    {
                                        "type": "string",
                                        "maxLength": 200,
                                        "example": "좋았던 점과 후속 작업을 정리합니다.",
                                    },
                                ),
                            ]
                        ),
                    },
                    "ErrorResponse": {
                        "type": "object",
                        "properties": {
                            "error": {
                                "type": "string",
                                "example": "노트를 찾을 수 없습니다",
                            }
                        },
                    },
                    "ValidationErrorResponse": {
                        "type": "object",
                        "properties": {
                            "errors": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["TITLE_REQUIRED", "CONTENT_REQUIRED"],
                            }
                        },
                    },
                    "HealthResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "ok"},
                        },
                    },
                    "HomeResponse": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "example": "Flask Study Notes Service에 오신 것을 환영합니다",
                            },
                            "description": {
                                "type": "string",
                                "example": "이 프로젝트는 Flask 기반 Git 워크플로 연습용입니다.",
                            },
                            "available_endpoints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["/", "/home", "/notes", "/api/notes", "/health"],
                            },
                        },
                    },
                }
            },
        },
    )

    @app.get("/")
    @app.get("/home")
    def home():
        """
        서비스의 기본 소개 정보를 반환한다.
        ---
        tags:
          - 공통
        summary: 서비스 소개 정보 조회
        description: 프로젝트 개요와 주요 엔드포인트 목록을 반환한다.
        responses:
          200:
            description: 프로젝트 소개 정보
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/HomeResponse'
        """
        return jsonify(
            {
                "message": "Welcome to the Flask Study Notes Service",
                "description": "This project is for practicing Git workflow with Flask.",
                "available_endpoints": [
                    "/",
                    "/home",
                    "/notes",
                    "/notes/<id>",
                    "/write",
                    "/api/notes",
                    "/health",
                    "/apidocs/",
                ],
            }
        )

    @app.get("/health")
    def health():
        """
        애플리케이션이 실행 중인지 확인한다.
        ---
        tags:
          - 공통
        summary: 헬스 체크
        responses:
          200:
            description: 서비스 상태 정보
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/HealthResponse'
        """
        return jsonify({"status": "ok"})

    note_service = NoteService(
        initial_notes=[
            Note(id=1, title="Welcome note", content="This is a default note for manual testing."),
            Note(id=2, title="Second welcome note", content="Add your own note through the API."),
        ]
    )
    form_spec = NoteFormSpec()
    note_controller = NoteController(note_service, form_spec)
    note_controller.register_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
