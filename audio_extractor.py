import ffmpeg
import os

def extract_audio(video_path: str) -> str:
    """Extract audio from video file"""
    audio_path = "temp_audio.wav"
    
    print(f"🎬 Extracting audio from: {video_path}")
    print("⚙️ Converting to 16kHz mono WAV for optimal Whisper performance...")
    
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Get file size for feedback
        import os
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
        print(f"✅ Audio extracted successfully ({file_size:.1f} MB)")
        
        return audio_path
    except Exception as e:
        print(f"❌ Audio extraction failed: {e}")
        raise Exception(f"Audio extraction failed: {e}")
