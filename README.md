# Automatic Subtitle Generator

Ein Python-Script zur automatischen Untertitel-Generierung aus Videos mit OpenAI Whisper.

**🎯 Converts any video to SRT subtitle files with German language support**

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

```bash
# Convert any video to SRT subtitles
python main.py path/to/your/video.mp4

# Example with test video
python main.py test_videos/test5-de.mp4
```

**That's it!** Your SRT subtitle file will be saved in the `output/` folder.

---

## ✨ Features

- 🎥 **Video Support:** MP4, AVI, MOV, MKV, and more
- 🇩🇪 **German Language:** Optimized for German speech recognition
- ⚡ **Fast Processing:** Efficient Whisper 'small' model
- 📝 **SRT Output:** Standard subtitle format compatible with all players
- 🔧 **Easy Setup:** One-command installation with SSL fixes included
- 📊 **Progress Tracking:** Real-time processing updates
- 🏷️ **Keyword Extraction:** Optional keyword extraction with KeyBERT

---

## 📁 Project Structure

```text
real-time-media-systems/
├── main.py              # 🎯 Main entry point
├── audio_extractor.py   # 🎵 Video → Audio conversion
├── srt_generator.py     # 📝 Whisper → SRT generation
├── keyword_extractor.py # 🏷️ Optional keyword extraction
├── requirements.txt     # 📦 Python dependencies
├── setup.sh            # ⚙️ Automatic setup script
├── test_videos/        # 🎬 Sample videos for testing
└── output/             # 📄 Generated SRT files
```

---

## 💻 Usage Examples

### Basic Usage

```bash
# Convert a single video
python main.py my_video.mp4

# Convert with full path
python main.py /path/to/your/video.mp4

# The SRT file will be saved as:
# output/my_video.srt
```

### Supported Formats

- **Input:** MP4, AVI, MOV, MKV (all ffmpeg-compatible formats)
- **Output:** SRT subtitle files (UTF-8 encoded)

---

## ⚙️ Configuration

### Whisper Model Sizes

You can adjust the Whisper model in `srt_generator.py` for different speed/quality trade-offs:

```python
# Available models (speed vs. accuracy):
model = whisper.load_model("tiny")    # Fastest
model = whisper.load_model("base")    # Standard
model = whisper.load_model("small")   # ⭐ Currently used (best balance)
model = whisper.load_model("medium")  # Better quality
model = whisper.load_model("large")   # Best quality, slowest
```

### Language Settings

Default is German. Change in `srt_generator.py`:

```python
result = model.transcribe(audio_path, language="de")  # German
result = model.transcribe(audio_path, language="en")  # English
result = model.transcribe(audio_path, language=None)  # Auto-detect
```

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

The project includes sample videos in `test_videos/`:

- `test5-de.mp4` - German test video
- `test4-de.mp4` - German test video
- `test3.mp4` - Short test (3m42s)

### Quality Checklist

- [ ] SRT file opens in video player (VLC, etc.)
- [ ] Subtitles are roughly synchronized (±2 seconds OK)
- [ ] German umlauts display correctly
- [ ] No empty subtitle segments

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

## 📚 Documentation

- **Technical Details:** See `TECHNICAL-DOCUMENTATION.md`
- **Project Planning:** See `Mini-MVP.md`
- **Development Status:** See `PROJECT-STATUS.md`

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