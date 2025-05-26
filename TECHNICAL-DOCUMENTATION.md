# Technical Documentation: Whisper STT Proof of Concept

**Ziel:** Automatische Untertitel-Generierung und Keyword-Extraktion für BHT-Videoplattform

---

## 1. Problemstellung und Zielsetzung

### Hauptziel
- Barrierefreie Videos durch automatische Untertitel-Generierung
- Verbesserung der Zugänglichkeit von Vorlesungsvideos
- Automatische Kapitel-Timestamps durch Keyword-Extraktion (Nice-to-have)

### Herausforderungen
- Kein direkter Zugriff auf Opencast/HRZ-System
- Deutsche Sprache mit Fachvokabular
- Verschiedene Dialekte und Sprechgeschwindigkeiten
- Integration in bestehende Plattformen (Moodle, BHT-Videoplattform)

---

## 2. Technologie-Vergleich: Speech-to-Text-Systeme

### Cloud-basierte Lösungen

#### Google Cloud Speech-to-Text
- **Vorteile:**
  - Exzellente Deutsch-Unterstützung
  - Echtzeit-Verarbeitung möglich
  - Automatische Punktuation und Diarisierung
  - Hohe Genauigkeit bei Fachsprache
- **Nachteile:**
  - Kosten bei größeren Mengen
  - Datenschutz-Bedenken (Cloud-Verarbeitung)
  - Internetverbindung erforderlich
- **Kosten:** ~$0.006 pro 15-Sekunden-Segment
- **API-Integration:** Sehr gut dokumentiert

#### Microsoft Azure Speech Services
- **Vorteile:**
  - Integrierte Keyword-Extraktion
  - Gute Deutsch-Unterstützung
  - Custom Speech Models möglich
  - Batch-Verarbeitung
- **Nachteile:**
  - Mittlere Preisklasse
  - Datenschutz-Aspekte
- **Kosten:** ~$1 pro Stunde Audio
- **Besonderheit:** Direkte Integration mit anderen Azure-Services

#### IBM Watson Speech to Text
- **Vorteile:**
  - Trainierbare Custom Models
  - Custom Dictionary für Fachbegriffe
  - Gute Enterprise-Integration
- **Nachteile:**
  - Höhere Kosten
  - Komplexere API
- **Kosten:** ~$0.02 pro Minute

### Open-Source/Lokale Lösungen

#### OpenAI Whisper ⭐ **EMPFEHLUNG**
- **Vorteile:**
  - Kostenlos und Open Source
  - Hervorragende Qualität für Deutsche Sprache
  - Läuft lokal (Datenschutz)
  - Verschiedene Model-Größen verfügbar
  - Aktive Community und Updates
- **Nachteile:**
  - Benötigt leistungsstarke Hardware für große Models
  - Keine Echtzeit-Verarbeitung
- **Models:** tiny, base, small, medium, large
- **Hardware-Anforderungen:** GPU empfohlen für large model

#### Vosk
- **Vorteile:**
  - Vollständig offline
  - Geringe Hardware-Anforderungen
  - Gute Python-Integration
- **Nachteile:**
  - Niedrigere Genauigkeit als Whisper
  - Begrenzte Deutsch-Models

---

## 3. Keyword-Extraktion: Technologien und Ansätze

### Regelbasierte Ansätze

#### spaCy + Named Entity Recognition
- **Vorteile:**
  - Lokale Verarbeitung
  - Gute Deutsch-Unterstützung
  - Erkennung von Fachbegrffen und Eigennamen
  - Team-Erfahrung vorhanden ⭐
- **Anwendung:** Extraktion von Personen, Organisationen, Fachbegriffen

#### YAKE (Yet Another Keyword Extractor)
- **Vorteile:**
  - Keine Trainingsdaten erforderlich
  - Statistische Methode
  - Gute Performance bei Fachtexten
- **Nachteile:**
  - Weniger kontextbezogen

### ML-basierte Ansätze

#### KeyBERT ⭐ **EMPFEHLUNG**
- **Vorteile:**
  - BERT-basiert, sehr gute Ergebnisse
  - Kontextbezogene Keyword-Extraktion
  - Einfache Integration mit STT-Output
  - Deutsche BERT-Models verfügbar
- **Anwendung:** Semantische Ähnlichkeit zwischen Dokument und Keywords

#### Cloud-basierte NLP-Services
- **Google Cloud Natural Language API**
- **Azure Text Analytics**
- **IBM Watson Natural Language Understanding**

---

## 4. Empfohlene Technologie-Stack

### Basis-Konfiguration (MVP)
```
Audio-Extraktion: ffmpeg
Speech-to-Text: OpenAI Whisper (small model)
Keyword-Extraktion: KeyBERT + spaCy
Untertitel-Format: SRT/VTT
Backend: Python (CLI-basiert)
```

### Erweiterte Konfiguration
- **STT-Alternativen:** Google Cloud Speech (für bessere Qualität)
- **Preprocessing:** Rauschunterdrückung mit librosa
- **Postprocessing:** Automatic Punctuation Restoration
- **Database:** PostgreSQL für Metadaten und Ergebnisse

---

## 5. Architektur und Workflow

### Verarbeitungspipeline

```
Video Upload → Audio-Extraktion → Speech-to-Text → Text-Postprocessing → 
Keyword-Extraktion → Timestamp-Zuordnung → Untertitel-Generierung → Export SRT
```

### Detaillierter Workflow

#### Phase 1: Audio-Verarbeitung
1. **Video-Input:** MP4, AVI, MOV, etc.
2. **Audio-Extraktion:** ffmpeg → WAV (16kHz, mono)
3. **Audio-Preprocessing:** 
   - Lautstärke-Normalisierung
   - Stille-Erkennung für bessere Segmentierung

#### Phase 2: Speech-to-Text
1. **Whisper-Verarbeitung:**
   ```python
   import whisper
   model = whisper.load_model("small")
   result = model.transcribe("audio.wav", language="de")
   ```
2. **Output:** Transkript mit Timestamps
3. **Postprocessing:** Fachbegriff-Glossar

#### Phase 3: Keyword-Extraktion
1. **KeyBERT-Verarbeitung:**
   ```python
   from keybert import KeyBERT
   kw_model = KeyBERT('distilbert-base-multilingual-cased')
   keywords = kw_model.extract_keywords(transcript, 
                                       keyphrase_ngram_range=(1, 3),
                                       stop_words='german')
   ```
2. **Timestamp-Zuordnung:** Keywords zu Videozeiten zuordnen

#### Phase 4: Output-Generierung
1. **SRT-Generierung:** Standard-Untertitelformat
2. **Keyword-Export:** JSON mit Timestamps und Beschreibungen

---

## 6. Implementierungsplan (MVP)

### Sprint 1: Basis-Pipeline ✅ (Abgeschlossen)
- [x] Setup Python-Environment
- [x] Audio-Extraktion mit ffmpeg implementieren
- [x] Whisper-Integration und erste Tests
- [x] Basis-SRT-Export

### Sprint 2: Optimierung und Tests (Aktuell)
- [x] Whisper 'small' model für bessere Deutsch-Qualität
- [x] Umfassendes Logging und Progress-Anzeigen
- [x] SSL-Zertifikat-Handling
- [ ] KeyBERT-Integration und Testing
- [ ] Performance-Optimierungen

### Sprint 3: Erweiterungen (Geplant)
- [ ] Batch-Processing für mehrere Videos
- [ ] Erweiterte Keyword-Extraktion
- [ ] Error-Handling und Logging
- [ ] Tests mit verschiedenen Videoformaten

---

## 7. Aktuelle Implementierung

### Projektstruktur
```
real-time-media-systems/
├── main.py              # Entry point mit CLI
├── audio_extractor.py   # Video → Audio (ffmpeg)
├── srt_generator.py     # Whisper → SRT
├── keyword_extractor.py # KeyBERT keyword extraction
├── requirements.txt     # Dependencies
├── setup.sh            # Cross-platform setup script
├── test_videos/        # Test files
└── output/             # Generated SRTs
```

### Abhängigkeiten
```python
openai-whisper==20231117  # Speech-to-text
ffmpeg-python==0.2.0      # Video processing  
keybert==0.8.4            # Keyword extraction
```

### Aktuelle Features
- ✅ Video zu Audio Konvertierung (ffmpeg)
- ✅ Speech-to-Text mit OpenAI Whisper 'small' model
- ✅ SRT-Untertitel Generation mit korrekten Timestamps
- ✅ Command-Line Interface
- ✅ SSL-Zertifikat-Handling für Whisper model downloads
- ✅ Umfassendes Logging und Progress-Anzeigen
- ✅ Keyword-Extraktion (KeyBERT) - implementiert aber optional

---

## 8. Performance und Testing

### Testdaten
Aktuelle Test-Videos verfügbar:
- `test3.mp4` (3m42s) - Kurzer Test
- `test4-de.mp4` - Deutsches Video
- `test5-de.mp4` - Deutsches Video
- `test1.mp4` (2h13m) - Langer Test
- `test2.mp4` (232MB) - Große Datei

### Performance (MacBook Pro M1)
- **3-4 Min Video:** ~45-60 Sekunden
- **15 Min Video:** ~3-4 Minuten  
- **2+ Stunden Video:** ~15-25 Minuten

### Whisper Model Vergleich
- **tiny:** Schnellstes, niedrigste Qualität
- **base:** Gute Balance, standard für Tests
- **small:** ⭐ Aktuell verwendet, bessere Deutsch-Qualität
- **medium:** Höhere Qualität, länger
- **large:** Beste Qualität, sehr langsam

---

## 9. Bekannte Probleme und Lösungen

### SSL-Zertifikat-Probleme
**Problem:** Whisper model download schlägt fehl  
**Lösung:** Integriert in `setup.sh` und `srt_generator.py`
```python
ssl._create_default_https_context = ssl._create_unverified_context
```

### Lange Verarbeitungszeiten
**Problem:** Große Videos dauern sehr lange  
**Lösungen:** 
- Verwendung von 'small' statt 'medium' model
- Audio-Kompression vor Verarbeitung
- Möglichkeit für 'tiny' model als Fallback

### Deutsche Umlaute
**Problem:** Encoding-Probleme in SRT-Files  
**Lösung:** UTF-8 encoding explizit gesetzt

---

## 10. Nächste Schritte

### Kurzfristig (Diese Woche)
1. **KeyBERT Integration** testen und optimieren
2. **Batch-Processing** für mehrere Videos
3. **Erweiterte Error-Handling**
4. **Performance-Optimierungen**

### Mittelfristig (Nächste Woche)
1. **Web-Interface** (optional)
2. **Integration verschiedener Whisper-Models**
3. **Umfangreiche Tests** mit verschiedenen Video-Typen
4. **Dokumentation vervollständigen**

---

## 11. Ressourcen und Links

### Dokumentation
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [KeyBERT Documentation](https://maartengr.github.io/KeyBERT/)
- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)

### Verwendete Models
- **Whisper 'small':** 461MB, optimiert für deutsche Sprache
- **KeyBERT:** distilbert-base-multilingual-cased

---

*Letzte Aktualisierung: Mai 26, 2025*  
*Status: MVP funktionsfähig, Optimierungen laufend*
