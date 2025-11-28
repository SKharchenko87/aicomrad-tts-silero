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
