#!/bin/bash

echo "Testing model mounting functionality..."

# Create models directory
mkdir -p models

# Download Russian model
echo "Downloading Russian model..."
curl -L https://models.silero.ai/models/tts/ru/v5_ru.pt -o models/model_ru.pt

# Start container with mounted models
echo "Starting container with mounted models..."
docker run -d -p 5002:5000 -v $(pwd)/models:/models --name silero-mount-test silero-tts

# Wait for server to start
echo "Waiting for server to start..."
sleep 10

# Check logs to verify mounted model is used
echo "Checking logs..."
docker logs silero-mount-test

# Cleanup
echo "Cleaning up..."
docker rm -f silero-mount-test

echo "Test complete!"
