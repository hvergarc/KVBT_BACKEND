import torchaudio
waveform, sample_rate = torchaudio.load("test.wav")
print("Loaded:", waveform.shape, sample_rate)
