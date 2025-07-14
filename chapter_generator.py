"""
Chapter generation and keyword extraction with YouTube-style timestamps
"""
import re
import nltk
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from keybert import KeyBERT
import textstat
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from utils import print_info, print_success, print_warning, console


class ChapterGenerator:
    """Generates YouTube-style chapters from subtitle content"""
    
    def __init__(self):
        self.keybert_model = None
        self.download_nltk_data()
    
    def download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print_info("Downloading language processing data...")
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
            except Exception as e:
                print_warning(f"Could not download NLTK data: {e}")
    
    def load_keybert_model(self):
        """Load KeyBERT model for keyword extraction"""
        if self.keybert_model is None:
            print_info("Loading keyword extraction model...")
            try:
                self.keybert_model = KeyBERT()
                print_success("Keyword extraction model loaded")
            except Exception as e:
                print_warning(f"Could not load KeyBERT model: {e}")
                return False
        return True
    
    def parse_srt_content(self, srt_path: str) -> List[Dict]:
        """Parse SRT file and extract subtitle data with timestamps"""
        try:
            with open(srt_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print_warning(f"Could not read SRT file: {e}")
            return []
        
        # Split by double newlines to separate subtitle blocks
        blocks = content.strip().split('\n\n')
        subtitles = []
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    # Extract number, timestamp, and text
                    number = int(lines[0].strip())
                    timestamp = lines[1].strip()
                    text = '\n'.join(lines[2:]).strip()
                    
                    # Parse timestamp
                    start_time, end_time = self.parse_timestamp(timestamp)
                    
                    subtitles.append({
                        'number': number,
                        'start_seconds': start_time,
                        'end_seconds': end_time,
                        'text': text,
                        'duration': end_time - start_time
                    })
                except (ValueError, IndexError):
                    continue
        
        return subtitles
    
    def parse_timestamp(self, timestamp_str: str) -> Tuple[float, float]:
        """Parse SRT timestamp format to seconds"""
        # Format: 00:00:20,000 --> 00:00:24,400
        start_str, end_str = timestamp_str.split(' --> ')
        
        def time_to_seconds(time_str):
            time_str = time_str.replace(',', '.')  # Replace comma with dot for milliseconds
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        
        return time_to_seconds(start_str), time_to_seconds(end_str)
    
    def create_text_segments(self, subtitles: List[Dict], segment_duration: int = 60) -> List[Dict]:
        """Group subtitles into larger text segments for analysis"""
        if not subtitles:
            return []
        
        segments = []
        current_segment = {
            'start_time': subtitles[0]['start_seconds'],
            'texts': [],
            'subtitle_indices': []
        }
        
        for i, subtitle in enumerate(subtitles):
            # Check if we should start a new segment
            if subtitle['start_seconds'] - current_segment['start_time'] >= segment_duration:
                if current_segment['texts']:
                    current_segment['end_time'] = subtitles[i-1]['end_seconds']
                    current_segment['combined_text'] = ' '.join(current_segment['texts'])
                    segments.append(current_segment)
                
                # Start new segment
                current_segment = {
                    'start_time': subtitle['start_seconds'],
                    'texts': [],
                    'subtitle_indices': []
                }
            
            current_segment['texts'].append(subtitle['text'])
            current_segment['subtitle_indices'].append(i)
        
        # Add the last segment
        if current_segment['texts']:
            current_segment['end_time'] = subtitles[-1]['end_seconds']
            current_segment['combined_text'] = ' '.join(current_segment['texts'])
            segments.append(current_segment)
        
        return segments
    
    def extract_keywords_from_segments(self, segments: List[Dict]) -> List[Dict]:
        """Extract keywords from each text segment"""
        if not self.load_keybert_model():
            return segments
        
        print_info(f"Extracting keywords from {len(segments)} segments...")
        
        for i, segment in enumerate(segments):
            try:
                # Extract keywords for this segment
                keywords = self.keybert_model.extract_keywords(
                    segment['combined_text'],
                    keyphrase_ngram_range=(1, 3),
                    stop_words='english',
                    top_n=5,
                    use_mmr=True,
                    diversity=0.5
                )
                
                segment['keywords'] = keywords
                segment['top_keyword'] = keywords[0][0] if keywords else f"Segment {i+1}"
                
            except Exception as e:
                print_warning(f"Could not extract keywords for segment {i+1}: {e}")
                segment['keywords'] = []
                segment['top_keyword'] = f"Segment {i+1}"
        
        return segments
    
    def detect_topic_changes(self, segments: List[Dict]) -> List[Dict]:
        """Detect major topic changes between segments using cosine similarity"""
        if len(segments) < 2:
            return segments
        
        print_info("Analyzing topic changes between segments...")
        
        # Extract text for vectorization
        texts = [segment['combined_text'] for segment in segments]
        
        try:
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Calculate similarity between consecutive segments
            similarities = []
            for i in range(len(segments) - 1):
                similarity = cosine_similarity(
                    tfidf_matrix[i:i+1], 
                    tfidf_matrix[i+1:i+2]
                )[0][0]
                similarities.append(similarity)
            
            # Mark segments with low similarity as topic changes
            # Use adaptive threshold based on similarity distribution
            if similarities:
                threshold = np.percentile(similarities, 25)  # Bottom 25%
                
                for i, similarity in enumerate(similarities):
                    segments[i+1]['topic_change'] = similarity < threshold
                    segments[i+1]['similarity_score'] = similarity
                
                # Always mark first segment as topic change
                segments[0]['topic_change'] = True
                segments[0]['similarity_score'] = 1.0
            
        except Exception as e:
            print_warning(f"Could not analyze topic changes: {e}")
            # Fallback: mark every few segments as topic changes
            for i, segment in enumerate(segments):
                segment['topic_change'] = i % 3 == 0
                segment['similarity_score'] = 0.5
        
        return segments
    
    def generate_chapter_titles(self, segments: List[Dict]) -> List[Dict]:
        """Generate meaningful chapter titles from keywords and content"""
        print_info("Generating chapter titles...")
        
        for segment in segments:
            if segment.get('topic_change', False):
                # This is a chapter start
                keywords = segment.get('keywords', [])
                
                if keywords:
                    # Use top keywords to create title
                    top_keywords = [kw[0] for kw in keywords[:3]]
                    
                    # Try to create a meaningful title
                    title = self.create_chapter_title(top_keywords, segment['combined_text'])
                    segment['chapter_title'] = title
                else:
                    # Fallback title
                    segment['chapter_title'] = f"Chapter {len([s for s in segments if s.get('topic_change', False)])}"
        
        return segments
    
    def create_chapter_title(self, keywords: List[str], text: str) -> str:
        """Create a meaningful chapter title from keywords and context"""
        # Simple heuristics for common lecture patterns
        text_lower = text.lower()
        
        # Look for common introduction/conclusion patterns
        if any(word in text_lower for word in ['introduction', 'intro', 'overview', 'beginning']):
            return "Introduction"
        elif any(word in text_lower for word in ['conclusion', 'summary', 'recap', 'ending']):
            return "Conclusion"
        elif any(word in text_lower for word in ['question', 'questions', 'q&a', 'discussion']):
            return "Questions & Discussion"
        
        # Use keywords to create title
        if keywords:
            # Capitalize and clean up keywords
            clean_keywords = []
            for keyword in keywords:
                # Remove special characters and capitalize
                clean_keyword = re.sub(r'[^a-zA-Z0-9\s]', '', keyword)
                clean_keyword = clean_keyword.title()
                if clean_keyword and len(clean_keyword) > 2:
                    clean_keywords.append(clean_keyword)
            
            if clean_keywords:
                if len(clean_keywords) == 1:
                    return clean_keywords[0]
                elif len(clean_keywords) == 2:
                    return f"{clean_keywords[0]} & {clean_keywords[1]}"
                else:
                    return f"{clean_keywords[0]} & {clean_keywords[1]}"
        
        return "New Topic"
    
    def format_timestamp_youtube(self, seconds: float) -> str:
        """Format timestamp for YouTube chapter format (MM:SS or H:MM:SS)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def generate_youtube_chapters(self, segments: List[Dict]) -> str:
        """Generate YouTube-style chapter timestamps"""
        chapters = []
        
        for segment in segments:
            if segment.get('topic_change', False):
                timestamp = self.format_timestamp_youtube(segment['start_time'])
                title = segment.get('chapter_title', 'New Chapter')
                chapters.append(f"{timestamp} {title}")
        
        return '\n'.join(chapters)
    
    def generate_chapter_summary(self, segments: List[Dict]) -> Dict:
        """Generate a comprehensive chapter summary"""
        chapters = []
        total_duration = 0
        
        for segment in segments:
            if segment.get('topic_change', False):
                chapter_info = {
                    'title': segment.get('chapter_title', 'New Chapter'),
                    'start_time': segment['start_time'],
                    'timestamp': self.format_timestamp_youtube(segment['start_time']),
                    'keywords': segment.get('keywords', []),
                    'similarity_score': segment.get('similarity_score', 0.0)
                }
                chapters.append(chapter_info)
        
        if segments:
            total_duration = segments[-1]['end_time']
        
        return {
            'total_chapters': len(chapters),
            'total_duration': total_duration,
            'chapters': chapters,
            'youtube_format': self.generate_youtube_chapters(segments)
        }
    
    def save_chapter_files(self, output_name: str, chapter_summary: Dict):
        """Save chapter information in multiple formats"""
        import os
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # YouTube format (for video descriptions)
        youtube_file = f"{output_dir}/{output_name}_chapters_youtube.txt"
        with open(youtube_file, 'w', encoding='utf-8') as f:
            f.write("YouTube Chapters (copy to video description):\n")
            f.write("=" * 50 + "\n\n")
            f.write(chapter_summary['youtube_format'])
            f.write("\n\n")
            f.write("Instructions:\n")
            f.write("1. Copy the timestamps above\n")
            f.write("2. Paste into your YouTube video description\n")
            f.write("3. YouTube will automatically create chapter markers\n")
        
        # Detailed chapter file
        detailed_file = f"{output_dir}/{output_name}_chapters_detailed.txt"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write(f"Detailed Chapter Analysis\\n")
            f.write("=" * 50 + "\\n\\n")
            f.write(f"Total Chapters: {chapter_summary['total_chapters']}\\n")
            f.write(f"Total Duration: {self.format_timestamp_youtube(chapter_summary['total_duration'])}\\n\\n")
            
            for i, chapter in enumerate(chapter_summary['chapters'], 1):
                f.write(f"Chapter {i}: {chapter['title']}\\n")
                f.write(f"  Timestamp: {chapter['timestamp']}\\n")
                f.write(f"  Topic Change Score: {chapter['similarity_score']:.3f}\\n")
                if chapter['keywords']:
                    f.write(f"  Keywords: {', '.join([kw[0] for kw in chapter['keywords'][:3]])}\\n")
                f.write("\\n")
        
        return youtube_file, detailed_file
    
    def process_srt_for_chapters(self, srt_path: str, output_name: str, 
                                segment_duration: int = 90) -> Dict:
        """Main function to process SRT file and generate chapters"""
        print_info("🔍 Analyzing subtitle content for chapter generation...")
        
        # Parse SRT file
        subtitles = self.parse_srt_content(srt_path)
        if not subtitles:
            print_warning("No subtitles found for chapter analysis")
            return {}
        
        print_info(f"Found {len(subtitles)} subtitle segments")
        
        # Create text segments for analysis
        segments = self.create_text_segments(subtitles, segment_duration)
        print_info(f"Created {len(segments)} text segments for analysis")
        
        # Extract keywords from each segment
        segments = self.extract_keywords_from_segments(segments)
        
        # Detect topic changes
        segments = self.detect_topic_changes(segments)
        
        # Generate chapter titles
        segments = self.generate_chapter_titles(segments)
        
        # Create chapter summary
        chapter_summary = self.generate_chapter_summary(segments)
        
        # Save chapter files
        if chapter_summary.get('chapters'):
            youtube_file, detailed_file = self.save_chapter_files(output_name, chapter_summary)
            chapter_summary['files'] = {
                'youtube': youtube_file,
                'detailed': detailed_file
            }
            
            print_success(f"Generated {chapter_summary['total_chapters']} chapters")
            print_info(f"YouTube format: {youtube_file}")
            print_info(f"Detailed analysis: {detailed_file}")
        
        return chapter_summary
    
    def show_chapter_preview(self, chapter_summary: Dict):
        """Display a preview of generated chapters"""
        if not chapter_summary.get('chapters'):
            print_warning("No chapters to display")
            return
        
        console.print(Panel.fit(
            "[bold blue]📺 Generated Chapters Preview[/bold blue]",
            border_style="blue"
        ))
        
        # Summary stats
        stats_table = Table(show_header=False, box=None, padding=(0, 1))
        stats_table.add_column(style="cyan")
        stats_table.add_column(style="white")
        
        total_duration = chapter_summary.get('total_duration', 0)
        stats_table.add_row("📊 Total chapters:", str(chapter_summary['total_chapters']))
        stats_table.add_row("⏱️ Total duration:", self.format_timestamp_youtube(total_duration))
        stats_table.add_row("📏 Avg chapter length:", 
                           self.format_timestamp_youtube(total_duration / chapter_summary['total_chapters']) 
                           if chapter_summary['total_chapters'] > 0 else "N/A")
        
        console.print(stats_table)
        console.print()
        
        # Chapter list
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Timestamp", style="cyan", width=10)
        table.add_column("Chapter Title", style="white", width=30)
        table.add_column("Top Keywords", style="yellow")
        
        for i, chapter in enumerate(chapter_summary['chapters'], 1):
            keywords = ", ".join([kw[0] for kw in chapter['keywords'][:3]]) if chapter['keywords'] else "N/A"
            
            table.add_row(
                str(i),
                chapter['timestamp'],
                chapter['title'],
                keywords
            )
        
        console.print(table)
        console.print()
        
        # YouTube format preview
        console.print("[bold cyan]YouTube Chapter Format:[/bold cyan]")
        console.print("[dim]Copy this to your YouTube video description:[/dim]")
        console.print()
        
        youtube_panel = Panel(
            chapter_summary['youtube_format'],
            title="YouTube Chapters",
            border_style="green"
        )
        console.print(youtube_panel)