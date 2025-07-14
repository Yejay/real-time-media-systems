import whisper
import os
import ssl
import subprocess
from datetime import timedelta
from tqdm import tqdm
from utils import ssl_workaround, format_duration, print_info, print_success, print_error, print_warning, create_progress_bar


def load_whisper_model(model_size: str = "small") -> whisper.Whisper:
    """Load Whisper model with fallback options
    
    Args:
        model_size: Size of the model to load (tiny, base, small, medium, large)
        
    Returns:
        whisper.Whisper: Loaded Whisper model
        
    Raises:
        Exception: If all model loading attempts fail
    """
    models_to_try = [model_size]
    if model_size != "base":
        models_to_try.append("base")
    if "tiny" not in models_to_try:
        models_to_try.append("tiny")
    
    for model_name in models_to_try:
        print_info(f"Attempting to load '{model_name}' model...")
        
        try:
            model = whisper.load_model(model_name)
            print_success(f"Whisper '{model_name}' model loaded successfully")
            return model
        except ssl.SSLError:
            print_warning("SSL Certificate error detected. Trying workaround...")
            try:
                with ssl_workaround():
                    model = whisper.load_model(model_name)
                    print_success(f"Model '{model_name}' loaded with SSL workaround")
                    return model
            except Exception as e:
                print_error(f"Failed to load '{model_name}' model with SSL workaround: {e}")
        except Exception as e:
            print_error(f"Failed to load '{model_name}' model: {e}")
    
    print_error("All model loading attempts failed")
    print_info("Try running: ./fix_ssl.sh")
    raise Exception("Could not load any Whisper model")


def get_audio_duration(audio_path: str) -> float:
    """Get audio file duration using ffprobe
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        float: Duration in seconds, or 0 if unable to determine
    """
    try:
        result = subprocess.run(
            ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', 
             '-v', 'quiet', '-of', 'csv=p=0'], 
            capture_output=True, text=True, timeout=10
        )
        return float(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError, FileNotFoundError):
        return 0.0


def transcribe_and_generate_srt(audio_path: str, output_name: str, 
                               model_size: str = "small", language: str = "de") -> str:
    """Transcribe audio and generate SRT file
    
    Args:
        audio_path: Path to audio file
        output_name: Base name for output files
        model_size: Whisper model size to use
        language: Language code for transcription
        
    Returns:
        str: Path to generated SRT file
    """
    model = load_whisper_model(model_size)
    
    # Get audio file info
    duration = get_audio_duration(audio_path)
    if duration > 0:
        print_info(f"Audio duration: {format_duration(duration)}")
        print_info(f"Estimated processing time: {format_duration(duration/4)}-{format_duration(duration/2)}")
    else:
        print_info("Audio duration: Unknown")
    
    # Transcribe
    print_info("Starting transcription... (this may take a while)")
    print_info("Whisper processes audio in 30-second chunks")
    
    # Create a custom progress callback for Whisper
    class WhisperProgressHook:
        def __init__(self):
            self.pbar = None
            
        def __call__(self, chunk):
            if self.pbar is None:
                # Estimate total chunks based on duration
                total_chunks = max(1, int(duration / 30)) if duration > 0 else 100
                self.pbar = tqdm(total=total_chunks, desc="Transcribing audio", unit="chunk")
            self.pbar.update(1)
            
        def close(self):
            if self.pbar:
                self.pbar.close()
    
    progress_hook = WhisperProgressHook()
    
    try:
        result = model.transcribe(audio_path, language=language, verbose=False)
        progress_hook.close()
        print_success(f"Transcription complete! Found {len(result['segments'])} segments")
    except Exception as e:
        progress_hook.close()
        raise e
    
    # Generate SRT
    print_info("Converting to SRT format...")
    srt_content = generate_srt_content(result["segments"])
    
    # Save SRT file
    srt_path = f"output/{output_name}.srt"
    os.makedirs("output", exist_ok=True)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    print_success(f"SRT file saved: {srt_path}")
    print_info(f"Generated {len(result['segments'])} subtitle segments")
    
    return srt_path

def generate_srt_content(segments) -> str:
    """Convert Whisper segments to SRT format with progress indication"""
    srt_content = ""
    
    with tqdm(segments, desc="Generating SRT", unit="segment") as pbar:
        for i, segment in enumerate(pbar, 1):
            start = seconds_to_srt_time(segment["start"])
            end = seconds_to_srt_time(segment["end"])
            text = segment["text"].strip()
            
            # Skip empty segments
            if not text:
                continue
                
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
