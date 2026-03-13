from flask import Flask, jsonify

app = Flask(__name__)

notes = [
    {"id": 1, "title": "Git Basics", "content": "Learn commit, branch, and merge."},
    {"id": 2, "title": "Flask Basics", "content": "Learn route and jsonify."},
    {"id": 3, "title": "Testing", "content": "Manual testing with curl."}
]


@app.route("/")
@app.route("/home")
def home():
    return jsonify({
        "message": "Welcome to the Flask Study Notes Service",
        "description": "This project is for practicing Git workflow with Flask.",
        "available_endpoints": [
            "/",
            "/home"
        ]
    })


@app.route("/notes")
def get_notes():
    return jsonify(notes)


@app.route("/notes/<int:note_id>")
def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return jsonify(note)

    return jsonify({"error": "Note not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)