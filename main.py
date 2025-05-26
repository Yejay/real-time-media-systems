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
    
    print("🚀 Whisper STT Pipeline Starting")
    print("=" * 40)
    print(f"📹 Input video: {video_file}")
    print(f"📄 Output name: {base_name}")
    print()
    
    # Check if video file exists
    if not os.path.exists(video_file):
        print(f"❌ Error: Video file not found: {video_file}")
        sys.exit(1)
    
    try:
        # Step 1: Extract audio
        print("🎵 STEP 1/3: Audio Extraction")
        print("-" * 30)
        audio_file = extract_audio(video_file)
        print()
        
        # Step 2: Generate SRT
        print("🤖 STEP 2/3: Speech Recognition")
        print("-" * 30)
        srt_file = transcribe_and_generate_srt(audio_file, base_name)
        print()
        
        # Step 3: Cleanup
        print("🧹 STEP 3/3: Cleanup")
        print("-" * 30)
        print("🗑️ Removing temporary audio file...")
        os.remove(audio_file)  # Delete temp audio
        print("✅ Cleanup complete")
        print()
        
        print("🎉 PROCESSING COMPLETE!")
        print("=" * 40)
        print(f"📁 SRT file saved to: {srt_file}")
        print("💡 You can now:")
        print(f"   - Open the SRT file: open {srt_file}")
        print(f"   - Test in VLC: Load both {video_file} and {srt_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user (Ctrl+C)")
        print("🧹 Cleaning up temporary files...")
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        print("✅ Cleanup complete")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("🧹 Cleaning up temporary files...")
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
        print("💡 Try running with a shorter video for testing")
        sys.exit(1)

if __name__ == "__main__":
    main()
