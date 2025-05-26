#!/usr/bin/env python3
"""
Minimal STT Pipeline
Usage: python main.py input_video.mp4
"""
import sys
import os
from audio_extractor import extract_audio
from srt_generator import transcribe_and_generate_srt

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <video_file>")
        sys.exit(1)
    
    video_file = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    
    print(f"Processing: {video_file}")
    
    # Step 1: Extract audio
    print("1/3 Extracting audio...")
    audio_file = extract_audio(video_file)
    
    # Step 2: Generate SRT
    print("2/3 Generating subtitles...")
    srt_file = transcribe_and_generate_srt(audio_file, base_name)
    
    # Step 3: Cleanup
    print("3/3 Cleaning up...")
    os.remove(audio_file)  # Delete temp audio
    
    print(f"✅ Done! SRT saved to: {srt_file}")

if __name__ == "__main__":
    main()
