# Silero TTS v5 Web UI

A modern web interface for Silero TTS v5, built with FastAPI and Docker.

## Features

- **High Quality TTS**: Uses the latest Silero v5 models.
- **Multi-Speaker**: Support for multiple voices (Russian/English).
- **Web Interface**: Clean, modern UI with dark mode.
- **Dockerized**: Easy to deploy with Docker.
- **Optimized**: CPU-only build for smaller image size.

## Quick Start

### Using Docker

1. Build the image:
   ```bash
   docker build -t silero-tts .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 silero-tts
   ```

3. Open [http://localhost:5000](http://localhost:5000)

### Using Pre-downloaded Models

To avoid downloading models on every container start, you can mount a directory with pre-downloaded models:

**Linux/macOS:**
```bash
# Create models directory and download models
mkdir models
curl -L https://models.silero.ai/models/tts/ru/v5_ru.pt -o models/model_ru.pt
curl -L https://models.silero.ai/models/tts/en/v3_en.pt -o models/model_en.pt

# Run with mounted models
docker run -p 5000:5000 -v $(pwd)/models:/models silero-tts
```

**Windows (PowerShell):**
```powershell
# Create models directory and download models
mkdir models
Invoke-WebRequest -Uri "https://models.silero.ai/models/tts/ru/v5_ru.pt" -OutFile "models/model_ru.pt"
Invoke-WebRequest -Uri "https://models.silero.ai/models/tts/en/v3_en.pt" -OutFile "models/model_en.pt"

# Run with mounted models
docker run -p 5000:5000 -v ${PWD}/models:/models silero-tts
```

**Note:** Model files must be named `model_ru.pt` and `model_en.pt` for the service to recognize them.

## Development

### Requirements
- Python 3.9+
- ffmpeg

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```
