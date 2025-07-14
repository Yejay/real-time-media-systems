"""
Subtitle preview functionality
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from datetime import timedelta
import re


console = Console()


def parse_srt_file(srt_path: str) -> list:
    """Parse SRT file and return list of subtitle entries"""
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by double newlines to separate subtitle blocks
        blocks = content.strip().split('\n\n')
        subtitles = []
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # Extract number, timestamp, and text
                number = lines[0].strip()
                timestamp = lines[1].strip()
                text = '\n'.join(lines[2:]).strip()
                
                # Parse timestamp
                start_time, end_time = parse_timestamp(timestamp)
                
                subtitles.append({
                    'number': int(number),
                    'start': start_time,
                    'end': end_time,
                    'text': text,
                    'duration': end_time - start_time
                })
        
        return subtitles
        
    except Exception as e:
        console.print(f"[red]Error parsing SRT file: {e}[/red]")
        return []


def parse_timestamp(timestamp_str: str) -> tuple:
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


def format_duration(seconds: float) -> str:
    """Format duration in seconds to mm:ss format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def show_subtitle_preview(srt_path: str, num_entries: int = 10):
    """Show a preview of the generated subtitles"""
    console.print(Panel.fit(
        "[bold blue]📺 Subtitle Preview[/bold blue]",
        border_style="blue"
    ))
    
    subtitles = parse_srt_file(srt_path)
    
    if not subtitles:
        console.print("[red]No subtitles found or error parsing file[/red]")
        return
    
    # Show statistics
    total_duration = max(sub['end'] for sub in subtitles)
    avg_duration = sum(sub['duration'] for sub in subtitles) / len(subtitles)
    
    stats_table = Table(show_header=False, box=None, padding=(0, 1))
    stats_table.add_column(style="cyan")
    stats_table.add_column(style="white")
    
    stats_table.add_row("📊 Total segments:", str(len(subtitles)))
    stats_table.add_row("⏱️  Total duration:", format_duration(total_duration))
    stats_table.add_row("📏 Average segment:", f"{avg_duration:.1f}s")
    
    console.print(stats_table)
    console.print()
    
    # Show first few subtitles
    preview_count = min(num_entries, len(subtitles))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Time", style="cyan", width=12)
    table.add_column("Duration", style="yellow", width=8)
    table.add_column("Text", style="white")
    
    for i in range(preview_count):
        sub = subtitles[i]
        start_time = format_duration(sub['start'])
        duration = f"{sub['duration']:.1f}s"
        
        # Truncate long text
        text = sub['text']
        if len(text) > 60:
            text = text[:57] + "..."
        
        # Replace newlines with spaces for table display
        text = text.replace('\n', ' ')
        
        table.add_row(
            str(sub['number']),
            start_time,
            duration,
            text
        )
    
    console.print(table)
    
    if len(subtitles) > preview_count:
        console.print(f"\n[dim]... and {len(subtitles) - preview_count} more segments[/dim]")
    
    # Show some quality metrics
    console.print()
    quality_panel = get_quality_metrics(subtitles)
    console.print(quality_panel)


def get_quality_metrics(subtitles: list) -> Panel:
    """Analyze subtitle quality and return metrics panel"""
    if not subtitles:
        return Panel("No subtitles to analyze", title="Quality Check")
    
    # Calculate various metrics
    total_segments = len(subtitles)
    empty_segments = sum(1 for sub in subtitles if not sub['text'].strip())
    short_segments = sum(1 for sub in subtitles if sub['duration'] < 1.0)
    long_segments = sum(1 for sub in subtitles if sub['duration'] > 10.0)
    
    # Character analysis
    total_chars = sum(len(sub['text']) for sub in subtitles)
    avg_chars = total_chars / total_segments if total_segments > 0 else 0
    
    # Create quality report
    quality_items = []
    
    # Empty segments check
    if empty_segments > 0:
        quality_items.append(f"⚠️  {empty_segments} empty segments detected")
    else:
        quality_items.append("✅ No empty segments")
    
    # Duration checks
    if short_segments > total_segments * 0.1:  # More than 10% are very short
        quality_items.append(f"⚠️  {short_segments} very short segments (<1s)")
    else:
        quality_items.append("✅ Good segment duration distribution")
    
    # Character count check
    if avg_chars < 10:
        quality_items.append(f"⚠️  Average text length is short ({avg_chars:.1f} chars)")
    elif avg_chars > 100:
        quality_items.append(f"⚠️  Average text length is long ({avg_chars:.1f} chars)")
    else:
        quality_items.append(f"✅ Good text length ({avg_chars:.1f} chars avg)")
    
    # Overall quality score
    issues = sum(1 for item in quality_items if item.startswith("⚠️"))
    if issues == 0:
        quality_items.append("\\n🎉 Excellent subtitle quality!")
    elif issues == 1:
        quality_items.append("\\n👍 Good subtitle quality with minor issues")
    else:
        quality_items.append("\\n🔍 Consider reviewing subtitle quality")
    
    quality_text = "\\n".join(quality_items)
    
    return Panel(
        quality_text,
        title="[bold green]Quality Check[/bold green]",
        border_style="green"
    )


def show_sample_subtitles(srt_path: str, start_time: float = 0, duration: float = 60):
    """Show subtitles for a specific time range"""
    console.print(f"[bold cyan]Showing subtitles from {format_duration(start_time)} for {duration}s[/bold cyan]")
    
    subtitles = parse_srt_file(srt_path)
    if not subtitles:
        return
    
    end_time = start_time + duration
    relevant_subs = [
        sub for sub in subtitles 
        if sub['start'] >= start_time and sub['start'] <= end_time
    ]
    
    if not relevant_subs:
        console.print("[yellow]No subtitles found in this time range[/yellow]")
        return
    
    for sub in relevant_subs:
        time_str = format_duration(sub['start'])
        console.print(f"[dim]{time_str}[/dim] {sub['text']}")