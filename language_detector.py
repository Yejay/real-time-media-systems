"""
Language detection functionality for automatic language identification
"""
import whisper
from typing import Optional, Dict, Tuple
from utils import print_info, print_success, print_warning, ssl_workaround


class LanguageDetector:
    """Handles automatic language detection using Whisper"""
    
    def __init__(self):
        self.language_names = {
            'en': 'English',
            'de': 'German',
            'es': 'Spanish', 
            'fr': 'French',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'cs': 'Czech',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'ca': 'Catalan',
            'eu': 'Basque',
            'gl': 'Galician',
            'cy': 'Welsh',
            'ga': 'Irish',
            'mt': 'Maltese',
            'is': 'Icelandic',
            'mk': 'Macedonian',
            'sq': 'Albanian',
            'af': 'Afrikaans',
            'az': 'Azerbaijani',
            'bn': 'Bengali',
            'bs': 'Bosnian',
            'eu': 'Basque',
            'fa': 'Persian',
            'he': 'Hebrew',
            'id': 'Indonesian',
            'ka': 'Georgian',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'lo': 'Lao',
            'mk': 'Macedonian',
            'ml': 'Malayalam',
            'mn': 'Mongolian',
            'ms': 'Malay',
            'my': 'Myanmar',
            'ne': 'Nepali',
            'ps': 'Pashto',
            'si': 'Sinhala',
            'sw': 'Swahili',
            'ta': 'Tamil',
            'te': 'Telugu',
            'th': 'Thai',
            'tl': 'Filipino',
            'ur': 'Urdu',
            'uz': 'Uzbek',
            'vi': 'Vietnamese',
            'yo': 'Yoruba'
        }
    
    def load_detection_model(self, model_size: str = "base") -> whisper.Whisper:
        """
        Load a Whisper model for language detection
        Uses a smaller model for faster detection
        """
        # Use base model for detection (faster than large models)
        detection_model = "base" if model_size in ["medium", "large"] else "tiny"
        
        print_info(f"Loading detection model '{detection_model}'...")
        
        try:
            model = whisper.load_model(detection_model)
            return model
        except Exception as e:
            print_warning(f"Failed to load {detection_model}, trying with SSL workaround...")
            try:
                with ssl_workaround():
                    model = whisper.load_model(detection_model)
                    return model
            except Exception as e2:
                raise Exception(f"Could not load detection model: {e2}")
    
    def detect_language(self, audio_path: str, model: Optional[whisper.Whisper] = None, 
                       duration_limit: int = 30) -> Tuple[str, float, Dict]:
        """
        Detect the language of an audio file
        
        Args:
            audio_path: Path to audio file
            model: Pre-loaded Whisper model (optional)
            duration_limit: Limit detection to first N seconds for speed
            
        Returns:
            Tuple of (language_code, confidence, detection_results)
        """
        if model is None:
            model = self.load_detection_model()
        
        print_info("🔍 Detecting language from audio sample...")
        
        try:
            # Load audio and detect language
            # Whisper's detect_language works on the first 30 seconds by default
            audio = whisper.load_audio(audio_path)
            
            # Limit to first N seconds for faster detection
            if duration_limit and len(audio) > duration_limit * whisper.audio.SAMPLE_RATE:
                audio = audio[:duration_limit * whisper.audio.SAMPLE_RATE]
            
            # Prepare audio for detection
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            
            # Detect language
            _, probs = model.detect_language(mel)
            
            # Get top language
            detected_language = max(probs, key=probs.get)
            confidence = probs[detected_language]
            
            return detected_language, confidence, probs
            
        except Exception as e:
            raise Exception(f"Language detection failed: {e}")
    
    def analyze_detection_results(self, language_code: str, confidence: float, 
                                all_probs: Dict) -> Dict:
        """
        Analyze detection results and provide recommendations
        
        Returns:
            Dictionary with analysis results
        """
        language_name = self.language_names.get(language_code, language_code.upper())
        
        # Get top 3 candidates
        top_candidates = sorted(all_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Determine confidence level
        if confidence >= 0.8:
            confidence_level = "High"
            recommendation = "proceed"
        elif confidence >= 0.5:
            confidence_level = "Medium" 
            recommendation = "proceed_with_caution"
        else:
            confidence_level = "Low"
            recommendation = "manual_review"
        
        return {
            'detected_language': language_code,
            'language_name': language_name,
            'confidence': confidence,
            'confidence_level': confidence_level,
            'recommendation': recommendation,
            'top_candidates': [
                (code, self.language_names.get(code, code.upper()), prob)
                for code, prob in top_candidates
            ]
        }
    
    def show_detection_results(self, analysis: Dict, show_alternatives: bool = True):
        """Display language detection results to user"""
        lang_name = analysis['language_name']
        lang_code = analysis['detected_language']
        confidence = analysis['confidence']
        confidence_level = analysis['confidence_level']
        
        if confidence >= 0.8:
            print_success(f"🎯 Detected language: {lang_name} ({lang_code}) - {confidence:.1%} confidence")
        elif confidence >= 0.5:
            print_warning(f"🤔 Detected language: {lang_name} ({lang_code}) - {confidence:.1%} confidence")
        else:
            print_warning(f"❓ Uncertain detection: {lang_name} ({lang_code}) - {confidence:.1%} confidence")
        
        print_info(f"📊 Confidence level: {confidence_level}")
        
        if show_alternatives and len(analysis['top_candidates']) > 1:
            print_info("🔍 Other possibilities:")
            for i, (code, name, prob) in enumerate(analysis['top_candidates'][1:], 2):
                if prob > 0.1:  # Only show significant alternatives
                    print_info(f"   {i}. {name} ({code}): {prob:.1%}")
        
        # Show recommendation
        if analysis['recommendation'] == 'manual_review':
            print_warning("💡 Recommendation: Consider manually specifying the language with --language")
            print_info("   Low confidence may indicate mixed languages or unclear audio")
        elif analysis['recommendation'] == 'proceed_with_caution':
            print_info("💡 Recommendation: Detection looks good, but verify results")
    
    def get_user_confirmation(self, analysis: Dict) -> Tuple[bool, Optional[str]]:
        """
        Ask user to confirm detected language or provide alternative
        
        Returns:
            Tuple of (use_detected, manual_language_code)
        """
        from utils import console
        
        lang_name = analysis['language_name']
        lang_code = analysis['detected_language']
        confidence = analysis['confidence']
        
        if confidence >= 0.8:
            # High confidence - just confirm
            response = console.input(f"\n✅ [green]Use detected language '{lang_name}' ({lang_code})? (Y/n): [/green]")
            if response.lower() in ['', 'y', 'yes']:
                return True, None
        else:
            # Lower confidence - ask for confirmation with alternatives
            console.print(f"\n🤔 [yellow]Detected '{lang_name}' ({lang_code}) with {confidence:.1%} confidence[/yellow]")
            
            # Show common alternatives
            console.print("Common options:")
            console.print("  • [cyan]y[/cyan] - Use detected language")
            console.print("  • [cyan]en[/cyan] - English")
            console.print("  • [cyan]de[/cyan] - German") 
            console.print("  • [cyan]es[/cyan] - Spanish")
            console.print("  • [cyan]fr[/cyan] - French")
            console.print("  • [cyan]auto[/cyan] - Let Whisper auto-detect during transcription")
            
            response = console.input("\nChoose language (or enter language code): ").strip().lower()
        
        if response in ['', 'y', 'yes']:
            return True, None
        elif response == 'auto':
            return False, None  # Use Whisper's auto-detection
        elif len(response) == 2 and response.isalpha():
            # Assume it's a language code
            return False, response
        else:
            # Default to detected
            print_info(f"Using detected language: {lang_name}")
            return True, None