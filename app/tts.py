import os
import torch
import hashlib
from typing import List, Optional
import soundfile as sf
import numpy as np

class SileroTTS:
    def __init__(self, model_path: str = "model.pt", device: str = "cpu"):
        self.device = torch.device(device)
        self.model = None
        self.sample_rate = 48000
        self.speakers = []
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        local_file = 'model.pt'
        if not os.path.isfile(local_file):
            print("Downloading model...")
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v5_ru.pt',
                                           local_file)  
        
        self.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.speakers = self.model.speakers

    def synthesize(self, text: str, speaker: str = 'xenia', sample_rate: int = 48000) -> str:
        """
        Synthesizes text to speech and returns the path to the generated audio file.
        Uses caching based on text and speaker.
        """
        # Generate cache key
        text_hash = hashlib.md5(f"{text}_{speaker}_{sample_rate}".encode()).hexdigest()
        output_dir = "cache"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{text_hash}.wav")

        if os.path.exists(output_path):
            return output_path

        audio = self.model.apply_tts(text=text,
                                     speaker=speaker,
                                     sample_rate=sample_rate)
        
        # Save to file
        sf.write(output_path, audio, sample_rate)
        return output_path

    def get_speakers(self) -> List[str]:
        return self.speakers
