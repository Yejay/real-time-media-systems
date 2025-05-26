# Mini-MVP: Automatische Untertitel-Generierung
**Timeline: 1 Woche (7 Tage)**  
**Ziel: Funktionierender Proof of Concept für Review**

---

## 🎯 Mini-MVP Scope (Absolutes Minimum)

### Was wird gebaut:
- ✅ **Einfaches Python-Script** das Videos zu SRT-Untertiteln konvertiert
- ✅ **Command-Line Interface** (kein Web-Interface)
- ✅ **Whisper für STT** (einfachste Integration)
- ✅ **Basic Keyword-Extraktion** (optional, nur wenn Zeit bleibt)

### Was NICHT gebaut wird:
- ❌ Web-Interface
- ❌ Database
- ❌ API
- ❌ Batch-Processing
- ❌ Error-Handling (nur Basics)

---

## 📅 1-Woche Sprint Plan

### Tag 1-2: Setup & Audio-Pipeline
**Ziel:** Video → Audio → Whisper funktioniert

#### Tasks Tag 1 (Setup)
- [ ] **Python Environment** erstellen
- [ ] **Whisper installieren** und testen
- [ ] **ffmpeg installieren** 
- [ ] **Erstes Test-Video** (5-10 Min) bereitstellen

#### Tasks Tag 2 (Audio-Pipeline)
- [ ] **audio_extractor.py** - Video zu Audio konvertieren
- [ ] **Whisper-Integration** - Audio zu Text
- [ ] **Test mit einem Video** - End-to-End

### Tag 3-4: SRT-Generation
**Ziel:** Whisper-Output wird zu korrektem SRT-File

#### Tasks Tag 3
- [ ] **SRT-Format verstehen** und implementieren
- [ ] **Timestamp-Konvertierung** (Whisper → SRT-Format)
- [ ] **srt_generator.py** erstellen

#### Tasks Tag 4  
- [ ] **Testing verschiedener Video-Längen**
- [ ] **Edge-Cases abfangen** (leere Segmente, etc.)
- [ ] **Code-Cleanup und Kommentare**

### Tag 5-6: Integration & Keywords (Optional)
**Ziel:** Alles zusammenbauen + evtl. simple Keywords

#### Tasks Tag 5
- [ ] **main.py** - Alles zusammenfügen
- [ ] **Command-Line Arguments** (input file, output folder)
- [ ] **Basic Error-Handling**

#### Tasks Tag 6 (Optional - nur wenn Zeit)
- [ ] **Simple Keyword-Extraktion** mit KeyBERT
- [ ] **Keywords in separates Text-File** exportieren

### Tag 7: Testing & Demo-Prep
**Ziel:** Bereit für Review

- [ ] **3-4 Test-Videos** verschiedener Längen durchlaufen lassen
- [ ] **README.md** mit Usage-Anleitung
- [ ] **Demo-Präsentation** vorbereiten

---

## 🛠 Minimal Tech-Stack

```python
# requirements.txt (nur 4-5 dependencies!)
openai-whisper==20231117
ffmpeg-python==0.2.0
keybert==0.8.4  # optional für Tag 6
```

---

## 📁 Minimal Projektstruktur

```
whisper-stt-poc/
├── main.py              # Entry point
├── audio_extractor.py   # Video → Audio
├── srt_generator.py     # Whisper → SRT
├── keyword_extractor.py # Optional
├── requirements.txt
├── README.md
├── test_videos/         # Test files
└── output/              # Generated SRTs
```

---

## 💻 Code-Templates (Starter)

### main.py (Ziel-Interface)
```python
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
```

### audio_extractor.py (Tag 1-2)
```python
import ffmpeg
import os

def extract_audio(video_path: str) -> str:
    """Extract audio from video file"""
    audio_path = "temp_audio.wav"
    
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except Exception as e:
        raise Exception(f"Audio extraction failed: {e}")
```

### srt_generator.py (Tag 3-4)
```python
import whisper
from datetime import timedelta

def transcribe_and_generate_srt(audio_path: str, output_name: str) -> str:
    """Transcribe audio and generate SRT file"""
    
    # Load Whisper model (start with 'base' for speed)
    model = whisper.load_model("base")
    
    # Transcribe
    result = model.transcribe(audio_path, language="de")
    
    # Generate SRT
    srt_content = generate_srt_content(result["segments"])
    
    # Save SRT file
    srt_path = f"output/{output_name}.srt"
    os.makedirs("output", exist_ok=True)
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    return srt_path

def generate_srt_content(segments) -> str:
    """Convert Whisper segments to SRT format"""
    srt_content = ""
    
    for i, segment in enumerate(segments, 1):
        start = seconds_to_srt_time(segment["start"])
        end = seconds_to_srt_time(segment["end"])
        text = segment["text"].strip()
        
        srt_content += f"{i}\n"
        srt_content += f"{start} --> {end}\n"
        srt_content += f"{text}\n\n"
    
    return srt_content

def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format (00:00:00,000)"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
```

---

## ✅ Daily Checkpoints

### Tag 1 Erfolg = 
- [ ] Whisper ist installiert und läuft
- [ ] Ein Test-Video kann zu Audio konvertiert werden
- [ ] Whisper kann das Audio transkribieren

### Tag 2 Erfolg =
- [ ] Script nimmt Video-File als Input
- [ ] Audio wird temporär extrahiert
- [ ] Whisper-Transkription funktioniert
- [ ] Text-Output wird angezeigt

### Tag 3 Erfolg =
- [ ] SRT-Format wird korrekt generiert
- [ ] Timestamps sind synchron
- [ ] SRT-File kann in VLC-Player geladen werden

### Tag 4 Erfolg =
- [ ] Verschiedene Video-Längen funktionieren
- [ ] Code ist sauber kommentiert
- [ ] Basic Error-Messages bei Problemen

### Tag 5 Erfolg =
- [ ] Command-Line Interface ist benutzerfreundlich
- [ ] Ein Video kann komplett verarbeitet werden
- [ ] Output-Ordner wird automatisch erstellt

### Tag 6 Erfolg (Optional) =
- [ ] Keywords werden extrahiert (KeyBERT)
- [ ] Keywords werden in Text-File gespeichert
- [ ] README ist geschrieben

### Tag 7 Erfolg =
- [ ] 3 verschiedene Test-Videos wurden erfolgreich verarbeitet
- [ ] Demo ist vorbereitet
- [ ] Code ist auf Git hochgeladen

---

## 🧪 Minimal Testing

### Test-Videos bereitstellen:
1. **Kurzes Video (2-3 Min)** - für schnelle Tests
2. **Mittleres Video (10-15 Min)** - realistische Vorlesung
3. **Deutsches Fachvideo** - z.B. YouTube-Informatik-Tutorial

### Manual Testing Checklist:
- [ ] SRT-File öffnet sich in Video-Player
- [ ] Untertitel sind grob synchron (±2 Sekunden OK)
- [ ] Deutsche Umlaute werden korrekt dargestellt
- [ ] Keine leeren Untertitel-Segmente

---

## 📋 Team-Aufteilung (3 Personen, 1 Woche)

### Person 1: Core-Pipeline
- **Tag 1-2:** Setup + audio_extractor.py
- **Tag 3-4:** srt_generator.py + Whisper-Integration
- **Tag 7:** Testing + Bugfixes

### Person 2: Integration + CLI
- **Tag 1-2:** Projektstruktur + requirements.txt
- **Tag 5-6:** main.py + Command-Line Interface
- **Tag 7:** README + Demo-Prep

### Person 3: Testing + Keywords
- **Tag 1-2:** Test-Videos sammeln + Installation-Testing
- **Tag 3-4:** Manual Testing der SRT-Qualität
- **Tag 5-6:** Keyword-Extraktion (optional)
- **Tag 7:** Final Testing + Dokumentation

---

## 🚀 Success-Kriterien für Review

### Minimum Viable Demo:
- [ ] **Command ausführen:** `python main.py test_video.mp4`
- [ ] **SRT-File wird generiert** in output/
- [ ] **SRT lädt in VLC** und Untertitel sind sichtbar
- [ ] **README erklärt** wie man es benutzt
- [ ] **3 Test-Videos** wurden erfolgreich verarbeitet

### Nice-to-have für Bonus-Punkte:
- [ ] Keywords werden zusätzlich extrahiert
- [ ] Code ist sauber und kommentiert
- [ ] Performance-Zeit wird gemessen und angezeigt
- [ ] Einfache Fehlerbehandlung (File nicht gefunden, etc.)

---

## 🔧 Setup-Anleitung (Day 1)

```bash
# 1. Python Environment
python -m venv whisper-env
source whisper-env/bin/activate  # Linux/Mac
# whisper-env\Scripts\activate   # Windows

# 2. Install Dependencies
pip install openai-whisper ffmpeg-python

# 3. Test Whisper
python -c "import whisper; print('Whisper installed!')"

# 4. Test ffmpeg
ffmpeg -version

# 5. Download first model
python -c "import whisper; whisper.load_model('base')"
```

---

**Nächster Schritt:** Sofort anfangen mit Day 1 Setup!  
**Review-Termin:** [Heute + 7 Tage]  
**Fallback:** Falls Probleme auftreten, auf Whisper "tiny" model wechseln für mehr Speed


cd /Users/yejay/dev/repos/university/real-time-media-systems && source whisper-env/bin/activate && python main.py test_videos/test5-de.mp4