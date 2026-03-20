from flask import Flask, jsonify

from client_validation import NoteFormSpec
from notes.note_controller import NoteController
from notes.note_service import NoteService


def create_app() -> Flask:
    _app = Flask(__name__)

    # 기존 Part 1 route는 유지
    @_app.get("/")
    @_app.get("/home")
    def home():
        return jsonify({
            "message": "Welcome to the Flask Study Notes Service",
            "description": "This project is for practicing Git workflow with Flask.",
            "available_endpoints": [
                "/",
                "/home"
            ]
        })

    @_app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    # TADD Step 1: contract objects only
    note_service = NoteService()
    form_spec = NoteFormSpec()
    note_controller = NoteController(note_service, form_spec)
    note_controller.register_routes(_app)

    return _app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)