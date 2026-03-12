let mediaRecorder;
let audioChunks = [];

async function startRecording() {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();

    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = sendAudioToServer;
}

function stopRecording() {
    mediaRecorder.stop();
}

function sendAudioToServer() {

    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

    const formData = new FormData();

    formData.append("audio", audioBlob, "recording.wav");

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {

            document.getElementById("result").innerText =
                "Predicted word: " + data.prediction;

        })
        .catch(error => console.error(error));
}