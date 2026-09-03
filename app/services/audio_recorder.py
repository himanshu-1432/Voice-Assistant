""" Audio recording utilities"""

import sounddevice as sd
import soundfile as sf
from app.config import config

def record_audio(duration:int,output_path:str)->str:
    """Record audio from microphone and save to file.

    Args:
        duration: Recording duration in seconds.
        output_path: Path to save the audio.

    returns:
        Path to saved audio files.
    """

    # Record Audio
    audio_data = sd.rec(
        int(duration * config.SAMPLE_RATE),
        samplerate=config.SAMPLE_RATE,
        channels=config.CHANNELS,
        dtype="float32"
    )

    # Wait for recording to finish
    sd.wait()

    # Save to file
    sf.write(output_path, audio_data, config.SAMPLE_RATE)
    return output_path


def play_audio(audio_path: str)->None:

    """Play an audio file.

    Args:
        audio_path: Path to audio file.
    """

    audio_data,sample_rate = sf.read(audio_path)
    sd.play(audio_data,sample_rate)
    sd.wait()