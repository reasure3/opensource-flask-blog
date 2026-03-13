from flask import Flask, jsonify

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)