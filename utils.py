"""
Utility functions for the subtitle generation pipeline
"""
import ssl
import tempfile
import os
from contextlib import contextmanager
from typing import Generator
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# Global console instance
console = Console()


@contextmanager
def ssl_workaround() -> Generator[None, None, None]:
    """
    Temporary SSL context workaround for model downloads
    
    This is needed on some systems where SSL certificate verification
    fails during Whisper model downloads.
    """
    original_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        yield
    finally:
        ssl._create_default_https_context = original_context


@contextmanager
def temp_audio_file() -> Generator[str, None, None]:
    """
    Create a temporary audio file and ensure cleanup
    
    Returns:
        str: Path to temporary audio file
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix='.wav', prefix='whisper_')
    try:
        os.close(temp_fd)  # Close file descriptor, keep the file
        print_info(f"Created temporary audio file: {os.path.basename(temp_path)}")
        yield temp_path
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print_info("Temporary files cleaned up")


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "2.3 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def print_header(title: str, subtitle: str = None):
    """Print a styled header"""
    if subtitle:
        text = Text(f"{title}\n{subtitle}", style="bold blue")
    else:
        text = Text(title, style="bold blue")
    
    console.print(Panel(text, style="blue"))


def print_step(step_num: int, total_steps: int, title: str, description: str = None):
    """Print a step header with progress"""
    step_text = f"[bold cyan]STEP {step_num}/{total_steps}: {title}[/bold cyan]"
    
    if description:
        step_text += f"\n[dim]{description}[/dim]"
    
    console.print("\n" + "─" * 50)
    console.print(step_text)
    console.print("─" * 50)


def print_success(message: str):
    """Print a success message"""
    console.print(f"✅ [green]{message}[/green]")


def print_error(message: str):
    """Print an error message"""
    console.print(f"❌ [red]{message}[/red]")


def print_warning(message: str):
    """Print a warning message"""
    console.print(f"⚠️ [yellow]{message}[/yellow]")


def print_info(message: str):
    """Print an info message"""
    console.print(f"ℹ️ [blue]{message}[/blue]")


def create_progress_bar():
    """Create a styled progress bar"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console
    )