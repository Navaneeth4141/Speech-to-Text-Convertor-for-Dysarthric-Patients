# DysarthriaSpeech AI

## Deep Learning Framework for Speech-to-Text Conversion in Dysarthric Patients

A web-based application that converts dysarthric speech to text using adaptive deep learning models, supporting communication and rehabilitation analysis.

![Status](https://img.shields.io/badge/status-academic%20prototype-blue)
![License](https://img.shields.io/badge/license-research%20only-yellow)

---

## 🌟 Features

- **🎤 Voice Recording** - Browser-based microphone capture with real-time waveform visualization
- **🧠 AI Transcription** - OpenAI Whisper-powered speech recognition optimized for dysarthric speech
- **📊 Comparison Mode** - Side-by-side baseline vs. fine-tuned ASR comparison
- **📈 Metrics Display** - Real-time WER/CER calculation with improvement tracking
- **♿ Accessibility** - Large text, dark mode, high contrast, keyboard navigation
- **🔒 Privacy First** - No audio storage, temporary processing only

---

## 🚀 Quick Start

### Frontend Only (Demo Mode)

1. Navigate to the `website/` folder
2. Open `index.html` in your browser
3. Click "Launch App" to access the speech-to-text interface
4. The app works in demo mode with simulated transcriptions

### Full Stack (With Backend)

#### Prerequisites
- Python 3.8+
- FFmpeg (optional, for audio processing)
- Modern web browser with microphone access

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The API will be available at `http://localhost:5000`

#### Frontend Setup

Simply open `website/index.html` in your browser, or serve with a local server:

```bash
# Using Python
cd website
python -m http.server 8080

# Then open http://localhost:8080
```

---

## 📁 Project Structure

```
Speech-to-Text-Convertor-for-Dysarthric-Patients
│
├── website/                         # Frontend application
│   ├── index.html                   # Landing page
│   ├── app.html                     # Main application interface
│   │
│   ├── styles/                      # CSS stylesheets
│   │   └── main.css                 # Main styling file
│   │
│   └── scripts/                     # JavaScript logic
│       ├── audio-recorder.js        # Handles microphone recording
│       ├── transcription.js         # Sends audio to backend API
│       ├── metrics.js               # Displays WER / CER metrics
│       ├── app.js                   # Main application logic
│       └── main.js                  # Landing page scripts
│
├── backend/                         # Python backend API
│   ├── app.py                       # Flask application entry point
│   ├── requirements.txt             # Python dependencies
│   │
│   └── services/                    # Core backend services
│       ├── audio_processor.py       # Audio preprocessing module
│       ├── speech_recognizer.py     # Whisper speech recognition integration
│       └── metrics.py               # Word Error Rate (WER) and Character Error Rate (CER)
│
├── PRD.pdf                          # Product Requirements Document
├── TRD.pdf                          # Technical Requirements Document
└── README.md                        # Project documentation

---

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/transcribe` | POST | Transcribe audio file |
| `/api/transcribe/compare` | POST | Transcribe with baseline comparison |
| `/api/health` | GET | Detailed service status |

### Example Request

```bash
curl -X POST http://localhost:5000/api/transcribe \
  -F "audio=@recording.wav" \
  -F "compare=true"
```

---

## 📊 Metrics

- **WER (Word Error Rate)**: Measures word-level transcription accuracy
- **CER (Character Error Rate)**: Measures character-level accuracy
- **Improvement**: Relative improvement of fine-tuned model over baseline

---

## ♿ Accessibility Features

- **Font Size Control**: Increase/decrease text size
- **Dark Mode**: Reduced eye strain in low light
- **High Contrast**: Clear visual distinction
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels throughout

---

## 🔬 Technical Details

### Audio Requirements
- Format: WebM (browser) → WAV (processing)
- Sample Rate: 16 kHz
- Channels: Mono

### Model
- Base: OpenAI Whisper (tiny/base/small)
- Fine-tuning: Transfer learning on dysarthric datasets

### Target Performance
- Transcription Latency: ≤1 second
- WER Improvement: ≥30% over baseline

---

## 📚 SDG Alignment

- **SDG 3**: Good Health & Well-Being (assistive healthcare)
- **SDG 4**: Quality Education (inclusive communication tools)

---

## ⚠️ Disclaimer

This is an **academic prototype** for research and educational purposes only.
- Not intended for clinical diagnosis
- No personal data storage
- Research use only

---

## 📝 License

Academic/Research Use Only

---

## 👥 Contributors

4th Semester SLAM Project
