#!/bin/bash

echo "🚀 Whisper STT Proof of Concept - Setup Script"
echo "=============================================="

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv whisper-env

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source whisper-env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check ffmpeg installation
echo "🎬 Checking ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is installed"
    ffmpeg -version | head -1
else
    echo "❌ ffmpeg not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "⚠️  Please install ffmpeg manually:"
        echo "   macOS: brew install ffmpeg"
        echo "   Ubuntu: sudo apt install ffmpeg"
    fi
fi

# Test Whisper installation
echo "🤖 Testing Whisper installation..."
python3 -c "import whisper; print('✅ Whisper installed successfully')" 2>/dev/null || echo "❌ Whisper installation failed"

# Download base model
echo "⬇️  Downloading Whisper base model..."
python3 -c "import whisper; whisper.load_model('base'); print('✅ Base model downloaded')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add a test video to test_videos/ folder"
echo "2. Run: python main.py test_videos/your_video.mp4"
echo "3. Check output/ folder for generated SRT file"
echo ""
echo "💡 To activate the environment later:"
echo "   source whisper-env/bin/activate"
