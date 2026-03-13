from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Flask Study Notes Service",
        "description": "This project is for practicing Git workflow with Flask.",
    })


if __name__ == "__main__":
    app.run(debug=True)