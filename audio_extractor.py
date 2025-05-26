import ffmpeg
import os

def extract_audio(video_path: str) -> str:
    """Extract audio from video file"""
    audio_path = "temp_audio.wav"
    
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except Exception as e:
        raise Exception(f"Audio extraction failed: {e}")
