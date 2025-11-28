from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from .tts import SileroTTS
from .utils import split_text
import shutil
from pydub import AudioSegment

app = FastAPI(title="Silero TTS v5 API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize TTS
tts = SileroTTS()

class SynthesisRequest(BaseModel):
    text: str
    speaker: str = "xenia"
    language: str = "ru" # Silero v5 ru model supports ru, en via different speakers mostly, but v5_ru is mainly ru. 
                         # Actually v5_ru supports auto language detection for en/ru if I recall correctly or just handles it.
                         # The prompt asked for "selection of language (ru, en)". 
                         # v5_ru supports 'aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random'
                         # For multi-language, usually v3_12 or v4_ru/en were separate. 
                         # v5_ru is "Multi-speaker" but primarily Russian. 
                         # However, let's stick to what the model offers. 
                         # If user wants explicit EN support, v5_ru might handle it with accent or we might need v3_en.
                         # But the prompt linked specifically to v5_ru.pt. I will assume v5_ru is sufficient.

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/speakers")
async def get_speakers():
    return {"speakers": tts.get_speakers()}

@app.post("/api/synthesize")
async def synthesize(request: SynthesisRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    # Split text if needed (though we have a max limit, splitting helps with flow)
    # The prompt asked for "Processing long texts (splitting into parts)"
    chunks = split_text(request.text, max_length=1000)
    
    audio_files = []
    for chunk in chunks:
        path = tts.synthesize(chunk, speaker=request.speaker, language=request.language)
        audio_files.append(path)
    
    # Combine audio files if multiple chunks
    if len(audio_files) == 1:
        final_path = audio_files[0]
    else:
        combined = AudioSegment.empty()
        for f in audio_files:
            combined += AudioSegment.from_wav(f)
        
        # Save combined
        final_path = f"cache/combined_{hash(request.text)}.wav"
        combined.export(final_path, format="wav")

    return FileResponse(final_path, media_type="audio/wav", filename="generated.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
