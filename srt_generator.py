import whisper
import os
from datetime import timedelta

def transcribe_and_generate_srt(audio_path: str, output_name: str) -> str:
    """Transcribe audio and generate SRT file"""
    
    # Load Whisper model (start with 'base' for speed)
    model = whisper.load_model("base")
    
    # Transcribe
    result = model.transcribe(audio_path, language="de")
    
    # Generate SRT
    srt_content = generate_srt_content(result["segments"])
    
    # Save SRT file
    srt_path = f"output/{output_name}.srt"
    os.makedirs("output", exist_ok=True)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    return srt_path

def generate_srt_content(segments) -> str:
    """Convert Whisper segments to SRT format"""
    srt_content = ""
    
    for i, segment in enumerate(segments, 1):
        start = seconds_to_srt_time(segment["start"])
        end = seconds_to_srt_time(segment["end"])
        text = segment["text"].strip()
        
        srt_content += f"{i}\n"
        srt_content += f"{start} --> {end}\n"
        srt_content += f"{text}\n\n"
    
    return srt_content

def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format (00:00:00,000)"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
