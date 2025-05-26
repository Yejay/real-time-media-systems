#!/bin/bash

# This script fixes SSL certificate issues for Whisper model downloads
# Only run this if you get SSL errors during initial setup
# After running once, this script is typically not needed again

echo "🔧 SSL Certificate Fix for Whisper (One-time setup)"
echo "=================================================="
echo "⚠️  Only run this if you get SSL certificate errors"
echo ""

# Option 1: Update certificates on macOS
echo "1️⃣ Updating macOS certificates..."
/Applications/Python\ 3.12/Install\ Certificates.command 2>/dev/null || echo "⚠️ Certificate installer not found, trying alternative..."

# Option 2: Download model manually with SSL workaround
echo "2️⃣ Downloading Whisper model manually..."
source whisper-env/bin/activate

# Download model with SSL verification disabled (temporary fix)
python3 -c "
import ssl
import whisper
ssl._create_default_https_context = ssl._create_unverified_context
try:
    whisper.load_model('base')
    print('✅ Base model downloaded successfully')
except Exception as e:
    print(f'❌ Download failed: {e}')
"

echo "3️⃣ Testing model availability..."
python3 -c "
import whisper
import os
# Check if model is cached locally
cache_dir = os.path.expanduser('~/.cache/whisper')
if os.path.exists(cache_dir):
    print(f'✅ Whisper cache found at: {cache_dir}')
    print('📁 Cached models:', os.listdir(cache_dir))
else:
    print('❌ No cached models found')
"

echo ""
echo "🎯 Ready to test again!"
echo "Run: python main.py test_videos/test1.mp4"
