#!/usr/bin/env python3
"""
Automatic Subtitle Generator using OpenAI Whisper
Usage: python main.py input_video.mp4 [--model MODEL_SIZE] [--language LANG_CODE]
"""
import sys
import os
import argparse
from pathlib import Path
from audio_extractor import extract_audio
from srt_generator import transcribe_and_generate_srt
from subtitle_preview import show_subtitle_preview
from batch_processor import BatchProcessor
from language_detector import LanguageDetector
from utils import temp_audio_file, print_header, print_step, print_success, print_error, print_info, console


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate subtitles from video files using OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python main.py video.mp4
  python main.py video.mp4 --model medium --language en
  python main.py /path/to/video.mp4 --model small --auto-detect
  python main.py videos/ --batch --recursive
  python main.py *.mp4 --batch --language auto"""
    )
    
    parser.add_argument(
        "video_files",
        nargs="+",
        help="Path(s) to video file(s), directories, or glob patterns to process"
    )
    
    parser.add_argument(
        "--model", 
        choices=["tiny", "base", "small", "medium", "large"],
        default="small",
        help="Whisper model size (default: small)"
    )
    
    parser.add_argument(
        "--language",
        default="de",
        help="Language code for transcription (default: de for German, 'auto' for detection)"
    )
    
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview and quality analysis of generated subtitles"
    )
    
    parser.add_argument(
        "--batch",
        action="store_true", 
        help="Enable batch processing mode for multiple files"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search directories recursively for video files"
    )
    
    parser.add_argument(
        "--auto-detect",
        action="store_true",
        help="Automatically detect language before processing"
    )
    
    return parser.parse_args()


def process_single_video(video_file: str, model_size: str, language: str, preview: bool) -> str:
    """Process a single video file and return the SRT file path"""
    base_name = Path(video_file).stem
    
    # Language detection if requested
    if language == "auto" or language == "detect":
        detector = LanguageDetector()
        
        with temp_audio_file() as temp_audio:
            # Extract a small sample for language detection
            print_step(1, 3, "Audio Extraction (Sample)", "Extracting audio sample for language detection")
            extract_audio(video_file, temp_audio)
            
            # Detect language
            print_step(2, 3, "Language Detection", "Analyzing audio to detect language")
            try:
                lang_code, confidence, all_probs = detector.detect_language(temp_audio)
                analysis = detector.analyze_detection_results(lang_code, confidence, all_probs)
                detector.show_detection_results(analysis)
                
                # Get user confirmation for uncertain detections
                if confidence < 0.8:
                    use_detected, manual_lang = detector.get_user_confirmation(analysis)
                    if not use_detected:
                        language = manual_lang if manual_lang else None
                    else:
                        language = lang_code
                else:
                    language = lang_code
                    
            except Exception as e:
                print_error(f"Language detection failed: {e}")
                print_info("Falling back to German (de)")
                language = "de"
    
    with temp_audio_file() as audio_file:
        # Step 1: Extract audio (full)
        step_num = 2 if language in ["auto", "detect"] else 1
        total_steps = 3 if language in ["auto", "detect"] else 2
        
        print_step(step_num, total_steps, "Audio Extraction", "Converting video to optimized audio format")
        extract_audio(video_file, audio_file)
        
        # Step 2: Generate SRT
        print_step(step_num + 1, total_steps, "Speech Recognition", f"Transcribing with {model_size} model")
        srt_file = transcribe_and_generate_srt(
            audio_file, base_name, model_size, language
        )
        
        return srt_file


def main():
    # Check if no arguments provided - launch interactive mode
    if len(sys.argv) == 1:
        try:
            from cli_menu import InteractiveCLI
            console.print("[bold blue]🚀 Launching Interactive Mode...[/bold blue]")
            console.print("[dim]Use 'python main.py --help' for command-line usage[/dim]\n")
            
            cli = InteractiveCLI()
            cli.run()
            return
        except ImportError:
            print_error("Interactive mode not available. Use command-line arguments.")
            print_info("Example: python main.py video.mp4")
            sys.exit(1)
    
    args = parse_arguments()
    
    # Handle batch processing
    if len(args.video_files) > 1 or args.batch:
        # Batch mode
        batch_processor = BatchProcessor()
        video_files = batch_processor.find_video_files(args.video_files, args.recursive)
        
        if not video_files:
            print_error("No video files found!")
            return
        
        # Confirm batch processing
        if not batch_processor.confirm_batch_processing(video_files):
            print_info("Batch processing cancelled.")
            return
        
        # Process batch
        def batch_process_func(video_file):
            return process_single_video(video_file, args.model, args.language, args.preview)
        
        results = batch_processor.process_batch(video_files, batch_process_func)
        batch_processor.show_batch_results()
        
        return
    
    # Single file mode
    video_file = args.video_files[0]
    
    # Print header with configuration
    print_header(
        "🚀 Automatic Subtitle Generator",
        "OpenAI Whisper-powered subtitle generation"
    )
    
    base_name = Path(video_file).stem
    print_info(f"Input video: {os.path.basename(video_file)}")
    print_info(f"Output name: {base_name}")
    print_info(f"Model: {args.model}")
    
    # Show language info
    if args.language in ["auto", "detect"] or args.auto_detect:
        print_info("Language: Auto-detection enabled")
        args.language = "auto"
    else:
        print_info(f"Language: {args.language}")
    
    # Check if video file exists
    if not os.path.exists(video_file):
        print_error(f"Video file not found: {video_file}")
        sys.exit(1)
    
    try:
        srt_file = process_single_video(video_file, args.model, args.language, args.preview)
        
        print_header("🎉 PROCESSING COMPLETE!", "Your subtitles are ready!")
        print_success(f"SRT file saved to: {srt_file}")
        
        # Show subtitle preview if requested
        if args.preview:
            console.print()
            show_subtitle_preview(srt_file)
        
        # Show final instructions
        console.print("\n📋 [bold cyan]Next Steps:[/bold cyan]")
        print_info(f"📁 SRT file location: {srt_file}")
        print_info("🎬 To use subtitles:")
        print_info("   1. Open your video in any player (VLC, IINA, etc.)")
        print_info("   2. Load the SRT file as external subtitles")
        print_info("   3. Or rename the SRT to match your video filename")
        
        console.print("\n✨ [green]Subtitle generation complete![/green]")
        
    except KeyboardInterrupt:
        print_info("\nProcess interrupted by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error occurred: {e}")
        print_info("Try running with a shorter video for testing")
        sys.exit(1)


if __name__ == "__main__":
    main()