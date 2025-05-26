import whisper
import os
import ssl
from datetime import timedelta

def transcribe_and_generate_srt(audio_path: str, output_name: str) -> str:
    """Transcribe audio and generate SRT file"""
    
    print("🤖 Loading Whisper model...")
    # Load Whisper model with SSL fix for macOS
    try:
        model = whisper.load_model("small")  # Changed from "base" to "small" for better German accuracy
        print("✅ Whisper 'small' model loaded successfully")
    except ssl.SSLError as e:
        print("⚠️ SSL Certificate error detected. Trying workaround...")
        # Temporary SSL fix for model download
        original_context = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            model = whisper.load_model("small")
            print("✅ Model loaded with SSL workaround")
        finally:
            # Restore original SSL context
            ssl._create_default_https_context = original_context
    except Exception as e:
        print(f"❌ Failed to load small model: {e}")
        print("🔄 Trying smaller 'base' model as fallback...")
        try:
            # Fallback to base model
            original_context = ssl._create_default_https_context
            ssl._create_default_https_context = ssl._create_unverified_context
            model = whisper.load_model("base")
            print("✅ Base model loaded successfully")
            ssl._create_default_https_context = original_context
        except Exception as e2:
            print(f"❌ All models failed: {e2}")
            print("💡 Try running: ./fix_ssl.sh")
            raise
    
    # Get audio file info
    try:
        import subprocess
        result_info = subprocess.run(['ffprobe', '-i', audio_path, '-show_entries', 
                                    'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], 
                                   capture_output=True, text=True)
        duration = float(result_info.stdout.strip())
        print(f"📊 Audio duration: {duration:.1f} seconds")
        print(f"⏱️ Estimated processing time: {duration/4:.1f}-{duration/2:.1f} seconds")
    except:
        print("📊 Audio duration: Unknown")
    
    # Transcribe
    print("🎤 Starting transcription... (this may take a while)")
    print("💡 Progress indicators:")
    print("   - Whisper processes audio in 30-second chunks")
    print("   - You'll see periodic progress updates")
    
    result = model.transcribe(audio_path, language="de", verbose=True)
    
    print(f"✅ Transcription complete! Found {len(result['segments'])} segments")
    
    # Generate SRT
    print("📝 Converting to SRT format...")
    srt_content = generate_srt_content(result["segments"])
    
    # Save SRT file
    srt_path = f"output/{output_name}.srt"
    os.makedirs("output", exist_ok=True)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    print(f"💾 SRT file saved: {srt_path}")
    print(f"📏 Generated {len(result['segments'])} subtitle segments")
    
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
