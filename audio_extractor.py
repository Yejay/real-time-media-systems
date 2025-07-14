import ffmpeg
import os
from utils import format_file_size, print_info, print_success, print_error, create_progress_bar


def extract_audio(video_path: str, output_path: str) -> str:
    """Extract audio from video file
    
    Args:
        video_path: Path to input video file
        output_path: Path for output audio file
        
    Returns:
        str: Path to extracted audio file
        
    Raises:
        Exception: If audio extraction fails
    """
    print_info(f"Source video: {os.path.basename(video_path)}")
    print_info("Converting to 16kHz mono WAV for optimal Whisper performance")
    
    with create_progress_bar() as progress:
        task = progress.add_task("Extracting audio...", total=None)
        
        try:
            (
                ffmpeg
                .input(video_path)
                .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')
                .overwrite_output()
                .run(quiet=True)
            )
            
            progress.update(task, completed=100)
            
            # Get file size for feedback
            file_size = os.path.getsize(output_path)
            print_success(f"Audio extracted successfully ({format_file_size(file_size)})")
            
            return output_path
            
        except Exception as e:
            progress.stop()
            print_error(f"Audio extraction failed: {e}")
            raise Exception(f"Audio extraction failed: {e}")
