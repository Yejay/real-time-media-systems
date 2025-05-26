#!/bin/bash

echo "🚀 Whisper STT Proof of Concept - Cross-Platform Setup"
echo "====================================================="

# Detect operating system
OS="Unknown"
case "$(uname -s)" in
    Darwin*)    OS="macOS";;
    Linux*)     OS="Linux";;
    CYGWIN*|MINGW*|MSYS*) OS="Windows";;
esac

echo "🖥️  Detected OS: $OS"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    python3 --version
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    python --version
    echo "⚠️  Using 'python' instead of 'python3'"
else
    echo "❌ Python not found! Please install Python 3.8+ first"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv whisper-env

# Activate virtual environment (cross-platform)
echo "⚡ Activating virtual environment..."
if [ "$OS" = "Windows" ]; then
    source whisper-env/Scripts/activate
else
    source whisper-env/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Platform-specific ffmpeg installation
echo "🎬 Checking ffmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is already installed"
    ffmpeg -version | head -1
else
    echo "❌ ffmpeg not found. Installing..."
    case "$OS" in
        "macOS")
            if command -v brew &> /dev/null; then
                echo "🍺 Installing ffmpeg via Homebrew..."
                brew install ffmpeg
            else
                echo "⚠️  Homebrew not found. Please install ffmpeg manually:"
                echo "   Visit: https://ffmpeg.org/download.html"
                echo "   Or install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            fi
            ;;
        "Linux")
            echo "🐧 Attempting to install ffmpeg via package manager..."
            if command -v apt &> /dev/null; then
                echo "   Using apt (Ubuntu/Debian)..."
                sudo apt update && sudo apt install -y ffmpeg
            elif command -v yum &> /dev/null; then
                echo "   Using yum (CentOS/RHEL)..."
                sudo yum install -y ffmpeg
            elif command -v dnf &> /dev/null; then
                echo "   Using dnf (Fedora)..."
                sudo dnf install -y ffmpeg
            elif command -v pacman &> /dev/null; then
                echo "   Using pacman (Arch)..."
                sudo pacman -S --noconfirm ffmpeg
            else
                echo "⚠️  Please install ffmpeg manually for your Linux distribution"
                echo "   Visit: https://ffmpeg.org/download.html"
            fi
            ;;
        "Windows")
            echo "🪟 Please install ffmpeg manually on Windows:"
            echo "   1. Download from: https://ffmpeg.org/download.html#build-windows"
            echo "   2. Extract and add to PATH"
            echo "   3. Or use chocolatey: choco install ffmpeg"
            ;;
    esac
fi

# SSL Certificate fix (especially for macOS)
echo "🔒 Setting up SSL certificates..."
case "$OS" in
    "macOS")
        echo "🍎 Applying macOS SSL certificate fix..."
        # Try to run the certificate installer
        if [ -f "/Applications/Python 3.12/Install Certificates.command" ]; then
            echo "   Running Python certificate installer..."
            /Applications/Python\ 3.12/Install\ Certificates.command 2>/dev/null || true
        elif [ -f "/Applications/Python 3.11/Install Certificates.command" ]; then
            echo "   Running Python certificate installer..."
            /Applications/Python\ 3.11/Install\ Certificates.command 2>/dev/null || true
        elif [ -f "/Applications/Python 3.10/Install Certificates.command" ]; then
            echo "   Running Python certificate installer..."
            /Applications/Python\ 3.10/Install\ Certificates.command 2>/dev/null || true
        else
            echo "   Certificate installer not found, updating certifi..."
            pip install --upgrade certifi
        fi
        ;;
    "Linux"|"Windows")
        echo "🔧 Updating certificates..."
        pip install --upgrade certifi
        ;;
esac

# Test Whisper installation
echo "🤖 Testing Whisper installation..."
$PYTHON_CMD -c "import whisper; print('✅ Whisper installed successfully')" 2>/dev/null || {
    echo "❌ Whisper installation test failed"
    echo "💡 This might be normal - continuing with model download..."
}

# Download Whisper model with SSL fallback
echo "⬇️  Downloading Whisper 'small' model (better German accuracy)..."
$PYTHON_CMD -c "
import ssl
import whisper
import sys

# First try normal download
try:
    model = whisper.load_model('small')
    print('✅ Small model downloaded successfully')
except ssl.SSLError as e:
    print('⚠️  SSL error detected, trying workaround...')
    # SSL workaround for problematic networks
    original_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        model = whisper.load_model('small')
        print('✅ Small model downloaded with SSL workaround')
    except Exception as e2:
        print(f'❌ Model download failed: {e2}')
        print('💡 You may need to download manually or check your internet connection')
        sys.exit(1)
    finally:
        ssl._create_default_https_context = original_context
except Exception as e:
    print(f'❌ Model download failed: {e}')
    print('💡 You may need to download manually or check your internet connection')
    sys.exit(1)
"

# Verify model cache
echo "📁 Checking model cache..."
$PYTHON_CMD -c "
import os
cache_dir = os.path.expanduser('~/.cache/whisper')
if os.path.exists(cache_dir):
    models = [f for f in os.listdir(cache_dir) if f.endswith('.pt')]
    if models:
        print(f'✅ Whisper models cached: {models}')
    else:
        print('⚠️  Cache directory exists but no models found')
else:
    print('⚠️  No whisper cache directory found')
"

# Final verification
echo "🧪 Running final verification..."
TEST_RESULT=$($PYTHON_CMD -c "
try:
    import whisper
    import ffmpeg
    print('success')
except Exception as e:
    print(f'error: {e}')
" 2>/dev/null)

if [ "$TEST_RESULT" = "success" ]; then
    echo "✅ All dependencies verified successfully!"
else
    echo "⚠️  Some issues detected: $TEST_RESULT"
    echo "💡 The pipeline might still work - try running a test"
fi

echo ""
echo "🎉 Setup complete!"
echo "================="
echo "📋 Next steps:"
echo "1. Add a test video to test_videos/ folder"
echo "2. Run: $PYTHON_CMD main.py test_videos/your_video.mp4"
echo "3. Check output/ folder for generated SRT file"
echo ""
echo "💡 To activate the environment later:"
if [ "$OS" = "Windows" ]; then
    echo "   source whisper-env/Scripts/activate  # Windows"
else
    echo "   source whisper-env/bin/activate      # macOS/Linux"
fi
echo ""
echo "🔧 Platform-specific notes:"
case "$OS" in
    "macOS")
        echo "   - ffmpeg installed via Homebrew"
        echo "   - SSL certificates updated"
        ;;
    "Linux")
        echo "   - ffmpeg installed via package manager"
        echo "   - May need sudo permissions for system packages"
        ;;
    "Windows")
        echo "   - ffmpeg needs manual installation"
        echo "   - Use Git Bash or WSL for best compatibility"
        ;;
esac
