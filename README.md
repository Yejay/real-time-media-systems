# Automatic Subtitle Generator

A Python application for automatically generating subtitles from video files using OpenAI Whisper, with advanced features like chapter generation and keyword extraction.

## 🎯 Features

- **🎥 Universal Video Support** - MP4, AVI, MOV, MKV, and all ffmpeg-compatible formats
- **🌍 Multi-Language** - Support for 90+ languages with auto-detection
- **⚡ Multiple AI Models** - Choose from tiny, base, small, medium, or large Whisper models
- **📝 Standard Output** - Generates SRT subtitle files compatible with all video players
- **📺 YouTube Chapters** - Automatically creates chapter timestamps for easy navigation
- **🏷️ Keyword Extraction** - Advanced keyword extraction with KeyBERT
- **🎮 Interactive Interface** - User-friendly menu system with file browser
- **📁 Batch Processing** - Process multiple videos at once
- **📊 Subtitle Preview** - Quality analysis and preview functionality

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** installed on your system
- **Git** (to clone the repository)

### 2. Installation

**⚠️ New Users: Run the automatic setup (recommended)**

```bash
# Clone the repository
git clone <repository-url>
cd real-time-media-systems

# One-command setup (handles everything automatically)
chmod +x setup.sh && ./setup.sh
```

**What the setup script does:**
- ✅ Creates isolated virtual environment (`whisper-env/`)
- ✅ Installs all Python dependencies (including chapter generation)
- ✅ Installs ffmpeg (audio extraction tool)
- ✅ Downloads Whisper AI model
- ✅ Fixes SSL certificate issues
- ✅ Tests everything works

**Manual Installation (if setup script fails):**

```bash
# Create virtual environment
python3 -m venv whisper-env
source whisper-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: Download from https://ffmpeg.org/
```

### 3. Understanding Virtual Environments

A virtual environment is like a **separate container** for this project:

- **🏠 Isolated** - Packages only affect this project, not your system
- **🔄 Reproducible** - Anyone can recreate the exact same setup
- **🛡️ Safe** - Won't break other Python projects or system Python
- **🧹 Clean** - Can delete `whisper-env/` folder to start fresh

You'll see `(whisper-env)` in your terminal prompt when activated.

### 4. Daily Usage

```bash
# Activate the virtual environment (do this every time)
source whisper-env/bin/activate

# Launch interactive mode (recommended)
python main.py

# Or use command line mode
python main.py path/to/video.mp4
```

### 5. Your First Video

1. **Interactive Mode (Easiest):**
   ```bash
   python main.py
   # Follow the menu to select video and configure settings
   ```

2. **Command Line Mode:**
   ```bash
   # Basic usage (auto-detect language, small model)
   python main.py test_videos/test5-de.mp4
   
   # With custom settings
   python main.py video.mp4 --model medium --language en --chapters
   ```

**Output:** Your SRT subtitle file will be saved in the `output/` folder!

---

## 🎮 Interactive Interface

The interactive mode provides a beginner-friendly menu system:

- **📂 File Browser** - Navigate and select videos easily
- **⚙️ Settings Menu** - Configure model, language, and features
- **📊 Recent Files** - Quick access to previously processed videos
- **💡 Built-in Help** - Examples and guidance

### Settings You Can Configure

| Setting | Options | Description |
|---------|---------|-------------|
| **Model** | tiny, base, small, medium, large | AI model size (speed vs quality) |
| **Language** | auto, en, de, es, fr, etc. | Target language or auto-detection |
| **Preview** | enabled/disabled | Show subtitle preview after generation |
| **Chapters** | enabled/disabled | Generate YouTube-style chapters |
| **Output** | custom directory | Where to save SRT files |

---

## ⌨️ Command Line Reference

### Basic Usage
```bash
python main.py video.mp4                    # Basic processing
python main.py video.mp4 --help             # Show all options
```

### Model Selection
```bash
python main.py video.mp4 --model tiny       # Fastest processing
python main.py video.mp4 --model small      # Default (recommended)
python main.py video.mp4 --model large      # Best quality
```

### Language Options
```bash
python main.py video.mp4 --language auto    # Auto-detect language
python main.py video.mp4 --language de      # German
python main.py video.mp4 --language en      # English
```

### Advanced Features
```bash
python main.py video.mp4 --chapters         # Generate YouTube chapters
python main.py video.mp4 --preview          # Show subtitle preview
python main.py videos/ --batch              # Process multiple videos
```

---

## 📺 Chapter Generation

Automatically creates YouTube-style chapter timestamps from your video content:

```bash
# Enable chapters in interactive mode or via command line
python main.py video.mp4 --chapters
```

**What it does:**
- 🔍 Analyzes subtitle content for topic changes
- 🏷️ Extracts keywords from each section using AI
- 📺 Creates YouTube-compatible chapter timestamps
- 📄 Generates ready-to-use files

**Output files:**
- `output/video_chapters_youtube.txt` - Ready to paste into YouTube description
- `output/video_chapters_detailed.txt` - Detailed analysis with keywords

**Example YouTube chapters:**
```
0:00 Introduction
2:30 Data Structures & Algorithms  
7:45 Machine Learning Basics
12:20 Neural Networks
18:10 Questions & Discussion
```

---

## 🌍 Language Support

### Automatic Detection
```bash
python main.py video.mp4 --language auto
```
- Analyzes first 30 seconds of audio
- Shows detected language with confidence level
- Asks for confirmation if confidence is low

### Supported Languages
Common language codes: `en` (English), `de` (German), `es` (Spanish), `fr` (French), `it` (Italian), `pt` (Portuguese), `ru` (Russian), `ja` (Japanese), `ko` (Korean), `zh` (Chinese)

**90+ total languages supported** including all major European, Asian, and world languages.

---

## 📊 Model Performance Guide

Choose the right model for your needs:

| Model | Speed | Quality | Memory | Use Case |
|-------|--------|---------|--------|----------|
| `tiny` | Fastest | Basic | Low | Quick tests, real-time |
| `base` | Fast | Good | Low | General use |
| `small` | Medium | Better | Medium | **Default** - Best balance |
| `medium` | Slow | High | High | High-quality transcription |
| `large` | Slowest | Best | Highest | Maximum accuracy |

### Processing Times (Reference: MacBook Pro M1)
- **3-4 minute video:** ~45-60 seconds (small model)
- **15 minute video:** ~3-4 minutes (small model)
- **1+ hour video:** ~15-25 minutes (small model)

---

## 📁 Using SRT Files

Generated SRT files work with all major video players:

### Automatic Loading (Easiest)
1. Rename SRT file to match your video: `my_video.mp4` → `my_video.srt`
2. Place both files in the same directory
3. Open video - subtitles load automatically

### Manual Loading
- **VLC:** Subtitle menu → Add Subtitle File
- **IINA:** Drag SRT file into player window
- **Any Player:** Right-click → Load Subtitles

### Troubleshooting Subtitles
- **Not showing?** Check if subtitles are enabled in player settings
- **Wrong encoding?** Ensure player uses UTF-8 encoding
- **Timing off?** Some players allow subtitle timing adjustment

---

## 🔧 Project Structure

```text
real-time-media-systems/
├── main.py              # Main entry point with CLI interface
├── cli_menu.py          # Interactive menu system
├── audio_extractor.py   # Video → Audio conversion
├── srt_generator.py     # Whisper → SRT generation
├── chapter_generator.py # YouTube chapter generation
├── keyword_extractor.py # Keyword extraction with KeyBERT
├── language_detector.py # Automatic language detection
├── subtitle_preview.py  # Subtitle preview and analysis
├── batch_processor.py   # Batch processing functionality
├── interactive.py       # Interactive mode launcher
├── utils.py             # Utility functions and helpers
├── requirements.txt     # All Python dependencies
├── setup.sh            # Automatic setup script
├── test_videos/        # Sample videos for testing
├── output/             # Generated SRT and chapter files
└── whisper-env/        # Virtual environment (created by setup)
```

---

## 🐛 Troubleshooting

### Setup Issues

**"Command not found" or "Module not found"**
```bash
# Problem: Virtual environment not activated
# Solution: Always activate first
source whisper-env/bin/activate
# You should see (whisper-env) in your prompt
```

**"No such file: whisper-env"**
```bash
# Problem: Setup script wasn't run
# Solution: Run setup script first
chmod +x setup.sh && ./setup.sh
```

**Environment corrupted or dependencies missing**
```bash
# Problem: Package conflicts or interrupted installation
# Solution: Delete and recreate environment
rm -rf whisper-env/
chmod +x setup.sh && ./setup.sh
```

**Different Python version issues**
```bash
# Problem: Multiple Python installations
# Solution: Specify Python version explicitly
python3.11 -m venv whisper-env  # or your preferred version
source whisper-env/bin/activate
pip install -r requirements.txt
```

### Runtime Issues

**ffmpeg not found**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian  
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/
```

**Whisper model download fails**
```bash
# Manually download model
python -c "import whisper; whisper.load_model('small')"
```

**German umlaut/special character issues**
- SRT files use UTF-8 encoding
- Set your video player to UTF-8 if problems persist

**Chapter generation not working**
```bash
# Ensure all dependencies are installed
source whisper-env/bin/activate
pip install -r requirements.txt
```

### Performance Issues

**Slow processing**
- Use `tiny` or `base` model for faster processing
- Ensure SSD storage for better I/O performance
- Close other applications to free up memory

**Out of memory errors**
- Use smaller model (`tiny` or `base`)
- Process shorter video segments
- Close other applications

---

## 🧪 Testing

### Test with Sample Videos
```bash
# Test with included sample videos
python main.py test_videos/test5-de.mp4

# Test different models
python main.py test_videos/test5-de.mp4 --model tiny
python main.py test_videos/test5-de.mp4 --model medium
```

### Quality Checklist
When testing generated subtitles:

- [ ] SRT file opens in video player
- [ ] Subtitles are synchronized with audio (±2 seconds acceptable)
- [ ] Special characters display correctly
- [ ] No empty or malformed subtitle segments
- [ ] Text is readable and accurate

---

## 🤝 Project Information

**Course:** Real-Time Media Systems  
**Team:** Yejay Demirkan, Marcus Schumann, Vasiliki Ioannidou  
**Semester:** SoSe 2025  
**Goal:** Automatic subtitle generation for university video platform

### Technologies Used
- **OpenAI Whisper** - State-of-the-art speech-to-text
- **KeyBERT** - Advanced keyword extraction
- **scikit-learn** - Machine learning for chapter detection
- **ffmpeg** - Audio/video processing
- **Rich** - Beautiful terminal interface

---

## 📄 License

This is a university project (Proof of Concept) for educational purposes.

---

*Last updated: July 2025*