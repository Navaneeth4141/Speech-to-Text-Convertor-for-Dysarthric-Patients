from flask import Flask, request, jsonify
import os

from services.speech_recognizer import predict

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/predict", methods=["POST"])
def predict_audio():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"})


    file = request.files["audio"]

    file = request.files["audio"]

    filepath = os.path.join(UPLOAD_FOLDER, "speech.webm")

    file.save(filepath)

    result = predict(filepath)

    return jsonify({"prediction": result})

    file.save(filepath)

    result = predict(filepath)

    return jsonify({"prediction": result})


if __name__ == "__main__":
    app.run(debug=True)