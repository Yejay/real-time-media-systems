# Automatic Subtitle Generator

A Python application for automatically generating subtitles from video files using OpenAI Whisper.

## 🎯 Converts any video to SRT subtitle files with multi-language support

---

## 🚀 Quick Start

Ready to use in under 2 minutes! Follow these steps:

### 1. Prerequisites

- Python 3.8+ installed on your system
- ffmpeg installed (for audio extraction)

### 2. Setup

```bash
# Run the setup script (handles everything automatically)
chmod +x setup.sh && ./setup.sh

# Activate the environment
source whisper-env/bin/activate
```

### 3. Convert your first video

**Interactive Mode (Recommended):**
```bash
# Launch interactive menu (easiest way)
python main.py

# Or use the dedicated interactive launcher
python interactive.py
```

**Command Line Mode:**
```bash
# Basic usage (German language, small model)
python main.py path/to/your/video.mp4

# With custom model and language
python main.py video.mp4 --model medium --language en

# Example with test video
python main.py test_videos/test5-de.mp4
```

**That's it!** Your SRT subtitle file will be saved in the `output/` folder.

### 4. Choose Your Interface

**🎮 Interactive Mode (Beginner-Friendly)**
- Menu-driven interface
- File browser and settings
- No need to remember commands
- Built-in help and examples

**⌨️ Command Line Mode (Advanced)**
- Fast for scripting and automation
- All features available via flags
- Perfect for batch operations
- Integration with other tools

---

## ✨ Features

- 🎥 **Video Support:** MP4, AVI, MOV, MKV, and more (all ffmpeg-compatible formats)
- 🌍 **Multi-Language:** Support for German, English, and auto-detection
- ⚡ **Multiple Models:** Choose from tiny, base, small, medium, or large Whisper models
- 📝 **SRT Output:** Standard subtitle format compatible with all players
- 🔧 **Easy Setup:** One-command installation with SSL fixes included
- 📊 **Progress Tracking:** Real-time processing updates
- 🗂️ **Smart Cleanup:** Automatic temporary file management
- 📊 **Subtitle Preview:** Quality analysis and preview functionality
- 📁 **Batch Processing:** Process multiple videos at once
- 🌍 **Auto Language Detection:** Automatically detect video language
- 🎮 **Interactive CLI:** User-friendly menu system
- 🏷️ **Keyword Extraction:** Optional keyword extraction with KeyBERT

---

## 📁 Project Structure

```text
real-time-media-systems/
├── main.py              # 🎯 Main entry point with CLI interface
├── audio_extractor.py   # 🎵 Video → Audio conversion
├── srt_generator.py     # 📝 Whisper → SRT generation
├── subtitle_preview.py  # 📊 Subtitle preview and analysis
├── batch_processor.py   # 📁 Batch processing functionality
├── language_detector.py # 🌍 Automatic language detection
├── cli_menu.py          # 🎮 Interactive CLI menu system
├── interactive.py       # 🎯 Interactive mode launcher
├── keyword_extractor.py # 🏷️ Optional keyword extraction
├── utils.py             # 🔧 Utility functions and helpers
├── requirements.txt     # 📦 Python dependencies
├── setup.sh            # ⚙️ Automatic setup script
├── test_videos/        # 🎬 Sample videos for testing
└── output/             # 📄 Generated SRT files
```

---

## 💻 Usage Examples

### 🎮 Interactive Mode (Recommended)

```bash
# Launch interactive menu
python main.py

# Follow the prompts:
# 1. Choose "Process Single Video" or "Batch Process Videos"
# 2. Select your video file(s) using the file browser
# 3. Configure settings (model, language, preview)
# 4. Start processing
```

**Interactive Features:**
- 📂 Built-in file browser
- ⚙️ Settings configuration menu
- 📊 Recent files history
- 🎯 Step-by-step guidance
- 💡 Built-in help and examples

### ⌨️ Command Line Mode

```bash
# Basic usage
python main.py my_video.mp4

# With custom settings
python main.py video.mp4 --model medium --language en

# Automatic language detection
python main.py video.mp4 --language auto

# Show subtitle preview
python main.py video.mp4 --preview

# Batch processing
python main.py videos/ --batch --recursive

# Get help
python main.py --help
```

### Supported Formats

- **Input:** MP4, AVI, MOV, MKV (all ffmpeg-compatible formats)
- **Output:** SRT subtitle files (UTF-8 encoded)

---

## ⚙️ Configuration

### Model Selection

Choose the appropriate Whisper model based on your needs:

| Model | Speed | Quality | Use Case |
|-------|--------|---------|----------|
| `tiny` | Fastest | Basic | Quick tests, real-time processing |
| `base` | Fast | Good | General use, faster processing |
| `small` | Medium | Better | **Default** - Best balance |
| `medium` | Slow | High | High-quality transcription |
| `large` | Slowest | Best | Maximum accuracy needed |

```bash
# Examples:
python main.py video.mp4 --model tiny     # Fastest processing
python main.py video.mp4 --model large    # Best quality
```

### Language Options

Specify the language for better accuracy:

```bash
python main.py video.mp4 --language de    # German (default)
python main.py video.mp4 --language en    # English
python main.py video.mp4 --language fr    # French
python main.py video.mp4 --language auto  # Auto-detect
```

Common language codes: `en` (English), `de` (German), `es` (Spanish), `fr` (French), `it` (Italian), `pt` (Portuguese), `ru` (Russian), `ja` (Japanese), `ko` (Korean), `zh` (Chinese)

### Automatic Language Detection

Let Whisper automatically detect the language:

```bash
python main.py video.mp4 --language auto        # Auto-detect language
python main.py video.mp4 --auto-detect          # Alternative flag
```

**How it works:**
- Analyzes first 30 seconds of audio
- Shows detected language with confidence level
- Asks for confirmation if confidence is low
- Falls back to manual selection if needed

**Supported languages:** 90+ languages including all major European, Asian, and world languages

---

## 📈 Performance

### Processing Times (MacBook Pro M1)

- **3-4 minute video:** ~45-60 seconds
- **15 minute video:** ~3-4 minutes
- **1+ hour video:** ~15-25 minutes

### Optimization Tips

- Use `tiny` model for quick tests
- Use `small` model for production (current default)
- SSD storage recommended for better I/O performance

---

## 🧪 Testing

### Test Videos Available

The project includes sample videos in `test_videos/` for testing different scenarios.

### Quality Checklist

When testing your generated subtitles:

- [ ] SRT file opens in video player (VLC, IINA, etc.)
- [ ] Subtitles are synchronized with audio (±2 seconds acceptable)
- [ ] Special characters display correctly (umlauts, accents, etc.)
- [ ] No empty or malformed subtitle segments
- [ ] Text is readable and makes sense

### Quick Test

```bash
# Test with included sample video
python main.py test_videos/test5-de.mp4

# Test with different models
python main.py test_videos/test5-de.mp4 --model tiny
python main.py test_videos/test5-de.mp4 --model medium
```

---

## 🐛 Troubleshooting

### Common Issues

**ffmpeg not found:**

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/
```

**Whisper model download fails:**

```bash
# Manually download model
python -c "import whisper; whisper.load_model('small')"
```

**German umlaut encoding issues:**

- SRT files are saved with UTF-8 encoding
- Set your video player to UTF-8 if problems persist

---

## 🔧 Advanced Usage

### Keyword Extraction

The script includes optional keyword extraction with KeyBERT:

```bash
# Keywords are automatically extracted and saved alongside SRT files
# See output/your_video_keywords.txt
```

### Batch Processing

Process multiple videos by running the script multiple times:

```bash
for video in test_videos/*.mp4; do
    python main.py "$video"
done
```

---

## 🎬 Using SRT Files with Video Players

The generated SRT files can be used with most video players to display subtitles. Here's how:

### Method 1: Same Filename (Automatic)

1. Rename the SRT file to match your video file name:

   ```bash
   # If your video is named my_lecture.mp4
   # Rename the SRT file to my_lecture.srt
   mv output/my_lecture.srt path/to/my_lecture.srt
   ```

2. Place both files in the same directory
3. Open the video file in your player - subtitles will load automatically

### Method 2: Manual Loading

#### In VLC Player

1. Open your video in VLC
2. Click on "Subtitle" in the menu
3. Select "Add Subtitle File..."
4. Browse and select your SRT file from the output folder

#### In IINA (macOS)

1. Open your video in IINA
2. Drag and drop the SRT file into the player window
   OR
3. Right-click → Subtitles → Open Subtitle File...
4. Select your SRT file from the output folder

### Method 3: Drag and Drop (Easiest)

1. Drag both the video file AND the SRT file into the player window simultaneously
2. The player will recognize them as a pair and load the subtitles automatically

### Troubleshooting Subtitle Display

- **Subtitles not showing:** Check if subtitles are enabled in the player settings
- **Encoding issues:** Make sure your player uses UTF-8 encoding for subtitles
- **Timing off:** Some players allow adjusting subtitle timing through settings
- **Wrong language:** Ensure correct language is selected in subtitle preferences

---

## 🤝 Project Info

**Course:** Real-Time Media Systems

**Team:** Yejay Demirkan, Marcus Schumann, Vasiliki Ioannidou

**Semester:** SoSe 2025

**Goal:** Automatic subtitle generation for university video platform

### Technologies Used

- **OpenAI Whisper** - Speech-to-text conversion
- **ffmpeg** - Audio extraction from video
- **KeyBERT** - Keyword extraction
- **Python 3.8+** - Core implementation

---

## 📄 License

This is a university project (Proof of Concept) for educational purposes.

---

*Last updated: May 26, 2025*
