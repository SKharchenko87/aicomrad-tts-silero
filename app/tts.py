import os
import torch
import hashlib
from typing import List, Optional
import soundfile as sf
import numpy as np

class SileroTTS:
    def __init__(self, device: str = "cpu"):
        self.device = torch.device(device)
        self.models = {}
        self.speakers = {}
        self.sample_rate = 48000
        self.model_urls = {
            "ru": "https://models.silero.ai/models/tts/ru/v5_ru.pt",
            "en": "https://models.silero.ai/models/tts/en/v3_en.pt"
        }
        # Preload Russian model by default as it's the main one
        self._load_model("ru")

    def _load_model(self, lang: str):
        if lang in self.models:
            return

        if lang not in self.model_urls:
            raise ValueError(f"Language {lang} not supported")

        model_filename = f"model_{lang}.pt"
        if not os.path.isfile(model_filename):
            print(f"Downloading {lang} model...")
            torch.hub.download_url_to_file(self.model_urls[lang], model_filename)
        
        model = torch.package.PackageImporter(model_filename).load_pickle("tts_models", "model")
        model.to(self.device)
        self.models[lang] = model
        self.speakers[lang] = model.speakers

    def synthesize(self, text: str, speaker: str = 'xenia', language: str = 'ru', sample_rate: int = 48000) -> str:
        """
        Synthesizes text to speech and returns the path to the generated audio file.
        Uses caching based on text and speaker.
        """
        # Ensure model is loaded
        self._load_model(language)

        # Validate speaker for the language
        if speaker not in self.speakers[language]:
            # Fallback to a default speaker if the requested one isn't available for this language
            if language == 'en':
                speaker = 'en_0'
            else:
                speaker = self.speakers[language][0] # Default to first available
            print(f"Speaker not found for {language}, defaulting to {speaker}")

        # Generate cache key
        text_hash = hashlib.md5(f"{text}_{speaker}_{language}_{sample_rate}".encode()).hexdigest()
        output_dir = "cache"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{text_hash}.wav")

        if os.path.exists(output_path):
            return output_path

        audio = self.models[language].apply_tts(text=text,
                                     speaker=speaker,
                                     sample_rate=sample_rate)
        
        # Save to file
        sf.write(output_path, audio, sample_rate)
        return output_path

    def get_speakers(self) -> dict:
        return self.speakers
