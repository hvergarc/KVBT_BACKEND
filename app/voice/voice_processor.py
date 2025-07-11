import torchaudio
import torch
from speechbrain.inference.speaker import SpeakerRecognition

class VoiceProcessor:
    def __init__(self):
        self.verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )

    def generate_voiceprint(self, audio_path):
        waveform, sample_rate = torchaudio.load(audio_path)
        embedding = self.verification.encode_batch(waveform)
        return embedding.squeeze().tolist()
    
    def compare_voiceprints(self, vp1, vp2):
        import numpy as np
        v1 = np.array(vp1)
        v2 = np.array(vp2)
        cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return float(cos_sim)
