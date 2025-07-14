"""
Interactive CLI menu system for the subtitle generator
"""
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from batch_processor import BatchProcessor
from language_detector import LanguageDetector
from utils import print_header, print_success, print_error, print_info, console


class InteractiveCLI:
    """Interactive command-line interface for subtitle generation"""
    
    def __init__(self):
        self.settings = {
            'model': 'small',
            'language': 'auto',
            'preview': True,
            'output_dir': 'output'
        }
        self.batch_processor = BatchProcessor()
        self.language_detector = LanguageDetector()
        self.recent_files = []
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        self.show_header()
        
        menu_options = [
            ("1", "🎬 Process Single Video", "Convert one video file to SRT subtitles"),
            ("2", "📁 Batch Process Videos", "Process multiple videos at once"),
            ("3", "⚙️  Settings", "Configure model, language, and options"),
            ("4", "📊 Recent Files", "View and reprocess recent files"),
            ("5", "ℹ️  Help & Info", "Show help and examples"),
            ("q", "🚪 Exit", "Quit the application")
        ]
        
        self.show_menu_table(menu_options)
        
        valid_choices = [opt[0] for opt in menu_options]
        choice = Prompt.ask(
            "\n[bold cyan]Choose an option[/bold cyan]",
            choices=valid_choices,
            default="1"
        )
        
        return choice
    
    def show_header(self):
        """Display application header"""
        header_text = Text()
        header_text.append("🚀 ", style="bold red")
        header_text.append("Automatic Subtitle Generator", style="bold blue")
        header_text.append("\n")
        header_text.append("OpenAI Whisper-powered subtitle generation", style="dim")
        
        header_panel = Panel(
            Align.center(header_text),
            style="blue",
            padding=(1, 2)
        )
        
        console.print(header_panel)
        console.print()
    
    def show_menu_table(self, options: List[tuple]):
        """Display menu options in a formatted table"""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Key", style="bold cyan", width=3)
        table.add_column("Option", style="bold white", width=25)
        table.add_column("Description", style="dim", width=40)
        
        for key, option, description in options:
            table.add_row(key, option, description)
        
        console.print(table)
    
    def show_settings_menu(self) -> bool:
        """Show settings configuration menu"""
        while True:
            console.clear()
            print_header("⚙️ Settings Configuration")
            
            # Current settings display
            settings_table = Table(show_header=True, header_style="bold magenta")
            settings_table.add_column("Setting", style="cyan")
            settings_table.add_column("Current Value", style="white")
            settings_table.add_column("Description", style="dim")
            
            settings_table.add_row(
                "Model", 
                self.settings['model'], 
                "Whisper model size (tiny/base/small/medium/large)"
            )
            settings_table.add_row(
                "Language", 
                self.settings['language'], 
                "Default language (auto for detection, de/en/etc.)"
            )
            settings_table.add_row(
                "Preview", 
                "✅ Enabled" if self.settings['preview'] else "❌ Disabled", 
                "Show subtitle preview after generation"
            )
            settings_table.add_row(
                "Output Directory", 
                self.settings['output_dir'], 
                "Directory for generated SRT files"
            )
            
            console.print(settings_table)
            console.print()
            
            menu_options = [
                ("1", "🤖 Change Model", "Select Whisper model size"),
                ("2", "🌍 Change Language", "Set default language or auto-detection"),
                ("3", "👁️  Toggle Preview", "Enable/disable subtitle preview"),
                ("4", "📁 Output Directory", "Change output directory"),
                ("5", "🔄 Reset to Defaults", "Reset all settings to defaults"),
                ("b", "⬅️  Back to Main Menu", "Return to main menu")
            ]
            
            self.show_menu_table(menu_options)
            
            choice = Prompt.ask(
                "\n[bold cyan]Configure setting[/bold cyan]",
                choices=["1", "2", "3", "4", "5", "b"],
                default="b"
            )
            
            if choice == "1":
                self.configure_model()
            elif choice == "2":
                self.configure_language()
            elif choice == "3":
                self.settings['preview'] = not self.settings['preview']
                status = "enabled" if self.settings['preview'] else "disabled"
                print_success(f"Preview {status}")
            elif choice == "4":
                self.configure_output_directory()
            elif choice == "5":
                if Confirm.ask("Reset all settings to defaults?"):
                    self.reset_settings()
                    print_success("Settings reset to defaults")
            elif choice == "b":
                return True
    
    def configure_model(self):
        """Configure Whisper model selection"""
        models = {
            "1": ("tiny", "Fastest, basic quality"),
            "2": ("base", "Fast, good quality"),
            "3": ("small", "Balanced (recommended)"),
            "4": ("medium", "Slow, high quality"),
            "5": ("large", "Slowest, best quality")
        }
        
        console.print("\n[bold cyan]Available Models:[/bold cyan]")
        model_table = Table(show_header=False, box=None, padding=(0, 2))
        model_table.add_column("Key", style="bold cyan", width=3)
        model_table.add_column("Model", style="bold white", width=10)
        model_table.add_column("Description", style="dim")
        
        for key, (model, desc) in models.items():
            current = " [green](current)[/green]" if model == self.settings['model'] else ""
            model_table.add_row(key, model + current, desc)
        
        console.print(model_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]Select model[/bold cyan]",
            choices=list(models.keys()),
            default="3"
        )
        
        self.settings['model'] = models[choice][0]
        print_success(f"Model set to: {self.settings['model']}")
        console.input("\nPress Enter to continue...")
    
    def configure_language(self):
        """Configure language settings"""
        languages = {
            "1": ("auto", "🤖 Auto-detect language"),
            "2": ("de", "🇩🇪 German"),
            "3": ("en", "🇺🇸 English"),
            "4": ("es", "🇪🇸 Spanish"),
            "5": ("fr", "🇫🇷 French"),
            "6": ("it", "🇮🇹 Italian"),
            "7": ("pt", "🇵🇹 Portuguese"),
            "8": ("custom", "✏️  Enter custom language code")
        }
        
        console.print("\n[bold cyan]Language Options:[/bold cyan]")
        lang_table = Table(show_header=False, box=None, padding=(0, 2))
        lang_table.add_column("Key", style="bold cyan", width=3)
        lang_table.add_column("Language", style="bold white", width=25)
        
        for key, (code, desc) in languages.items():
            current = " [green](current)[/green]" if code == self.settings['language'] else ""
            lang_table.add_row(key, desc + current)
        
        console.print(lang_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]Select language[/bold cyan]",
            choices=list(languages.keys()),
            default="1"
        )
        
        if choice == "8":
            custom_lang = Prompt.ask(
                "Enter language code (e.g., 'ru' for Russian, 'ja' for Japanese)",
                default=self.settings['language']
            )
            self.settings['language'] = custom_lang
        else:
            self.settings['language'] = languages[choice][0]
        
        print_success(f"Language set to: {self.settings['language']}")
        console.input("\nPress Enter to continue...")
    
    def configure_output_directory(self):
        """Configure output directory"""
        current_dir = self.settings['output_dir']
        console.print(f"\n[bold cyan]Current output directory:[/bold cyan] {current_dir}")
        
        new_dir = Prompt.ask(
            "Enter new output directory",
            default=current_dir
        )
        
        # Create directory if it doesn't exist
        try:
            Path(new_dir).mkdir(parents=True, exist_ok=True)
            self.settings['output_dir'] = new_dir
            print_success(f"Output directory set to: {new_dir}")
        except Exception as e:
            print_error(f"Could not create directory: {e}")
        
        console.input("\nPress Enter to continue...")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        self.settings = {
            'model': 'small',
            'language': 'auto',
            'preview': True,
            'output_dir': 'output'
        }
    
    def select_single_video(self) -> Optional[str]:
        """Interactive single video selection"""
        console.clear()
        print_header("🎬 Single Video Processing")
        
        # Show options for file selection
        options = [
            ("1", "📂 Browse for file", "Open file browser"),
            ("2", "✏️  Enter path manually", "Type file path"),
            ("3", "📋 Recent files", "Choose from recent files"),
            ("b", "⬅️  Back", "Return to main menu")
        ]
        
        self.show_menu_table(options)
        
        choice = Prompt.ask(
            "\n[bold cyan]How would you like to select the video?[/bold cyan]",
            choices=["1", "2", "3", "b"],
            default="2"
        )
        
        if choice == "1":
            return self.browse_for_file()
        elif choice == "2":
            return self.enter_file_path()
        elif choice == "3":
            return self.select_from_recent()
        elif choice == "b":
            return None
    
    def browse_for_file(self) -> Optional[str]:
        """Simple file browser (lists current directory)"""
        current_dir = Path.cwd()
        
        while True:
            console.clear()
            print_header(f"📂 Browse Files - {current_dir}")
            
            try:
                # List directories and video files
                items = []
                
                # Add parent directory option
                if current_dir != current_dir.parent:
                    items.append(("📁 ..", "directory", current_dir.parent))
                
                # Add subdirectories
                for item in sorted(current_dir.iterdir()):
                    if item.is_dir() and not item.name.startswith('.'):
                        items.append((f"📁 {item.name}/", "directory", item))
                
                # Add video files
                video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm', '.flv'}
                for item in sorted(current_dir.iterdir()):
                    if item.is_file() and item.suffix.lower() in video_extensions:
                        size = item.stat().st_size / (1024*1024)  # MB
                        items.append((f"🎬 {item.name} ({size:.1f} MB)", "video", item))
                
                # Display items
                if not items:
                    console.print("[yellow]No directories or video files found in this location.[/yellow]")
                else:
                    table = Table(show_header=False, box=None, padding=(0, 1))
                    table.add_column("Key", style="bold cyan", width=3)
                    table.add_column("Item", style="white")
                    
                    for i, (display_name, item_type, path) in enumerate(items, 1):
                        table.add_row(str(i), display_name)
                    
                    console.print(table)
                
                console.print(f"\n[dim]Current directory: {current_dir}[/dim]")
                
                # Get user choice
                if items:
                    choices = [str(i) for i in range(1, len(items) + 1)] + ["m", "b"]
                    choice = Prompt.ask(
                        "\n[bold cyan]Select item (m=manual entry, b=back)[/bold cyan]",
                        choices=choices
                    )
                    
                    if choice == "m":
                        return self.enter_file_path()
                    elif choice == "b":
                        return None
                    else:
                        idx = int(choice) - 1
                        display_name, item_type, selected_path = items[idx]
                        
                        if item_type == "directory":
                            current_dir = selected_path
                        elif item_type == "video":
                            return str(selected_path)
                else:
                    choice = Prompt.ask(
                        "\n[bold cyan]Options (m=manual entry, b=back)[/bold cyan]",
                        choices=["m", "b"]
                    )
                    
                    if choice == "m":
                        return self.enter_file_path()
                    elif choice == "b":
                        return None
                        
            except Exception as e:
                print_error(f"Error browsing directory: {e}")
                console.input("Press Enter to continue...")
                return None
    
    def enter_file_path(self) -> Optional[str]:
        """Manual file path entry"""
        console.print("\n[bold cyan]Enter video file path:[/bold cyan]")
        console.print("[dim]You can use Tab completion if your terminal supports it[/dim]")
        console.print("[dim]Examples: video.mp4, /path/to/video.mp4, ~/Downloads/lecture.mp4[/dim]")
        
        file_path = Prompt.ask(
            "\nFile path",
            default=""
        )
        
        if not file_path:
            return None
        
        # Expand user home directory
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            if Confirm.ask("Try again?"):
                return self.enter_file_path()
            return None
        
        if not os.path.isfile(file_path):
            print_error(f"Path is not a file: {file_path}")
            return None
        
        return file_path
    
    def select_from_recent(self) -> Optional[str]:
        """Select from recent files"""
        if not self.recent_files:
            print_info("No recent files found.")
            console.input("Press Enter to continue...")
            return None
        
        console.print("\n[bold cyan]Recent Files:[/bold cyan]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Key", style="bold cyan", width=3)
        table.add_column("File", style="white")
        table.add_column("Status", style="dim")
        
        for i, file_path in enumerate(self.recent_files, 1):
            exists = "✅" if os.path.exists(file_path) else "❌"
            table.add_row(str(i), os.path.basename(file_path), f"{exists} {file_path}")
        
        console.print(table)
        
        choices = [str(i) for i in range(1, len(self.recent_files) + 1)] + ["b"]
        choice = Prompt.ask(
            "\n[bold cyan]Select file (b=back)[/bold cyan]",
            choices=choices
        )
        
        if choice == "b":
            return None
        
        selected_file = self.recent_files[int(choice) - 1]
        
        if not os.path.exists(selected_file):
            print_error("File no longer exists!")
            console.input("Press Enter to continue...")
            return None
        
        return selected_file
    
    def add_to_recent_files(self, file_path: str):
        """Add file to recent files list"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        self.recent_files.insert(0, file_path)
        
        # Keep only last 10 files
        self.recent_files = self.recent_files[:10]
    
    def show_help(self):
        """Show help and examples"""
        console.clear()
        print_header("ℹ️ Help & Information")
        
        help_sections = [
            ("🎯 Quick Start", [
                "1. Select 'Process Single Video' from main menu",
                "2. Choose or enter your video file path",
                "3. Confirm settings and start processing",
                "4. Find generated .srt file in output directory"
            ]),
            ("🤖 Models", [
                "• tiny: Fastest, basic quality (~1-2 min for 10min video)",
                "• small: Recommended balance (~2-3 min for 10min video)",  
                "• medium: High quality (~4-5 min for 10min video)",
                "• large: Best quality (~8-10 min for 10min video)"
            ]),
            ("🌍 Languages", [
                "• auto: Automatically detect language",
                "• de: German (optimized for lectures)",
                "• en: English",
                "• 90+ other languages supported"
            ]),
            ("📁 Supported Formats", [
                "• MP4, AVI, MOV, MKV (most common formats)",
                "• Any format supported by ffmpeg",
                "• Output: SRT subtitle files (UTF-8)"
            ])
        ]
        
        for title, items in help_sections:
            console.print(f"\n[bold cyan]{title}[/bold cyan]")
            for item in items:
                console.print(f"  {item}")
        
        console.input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                console.clear()
                choice = self.show_main_menu()
                
                if choice == "1":
                    self.handle_single_video()
                elif choice == "2":
                    self.handle_batch_processing()
                elif choice == "3":
                    self.show_settings_menu()
                elif choice == "4":
                    self.show_recent_files()
                elif choice == "5":
                    self.show_help()
                elif choice == "q":
                    console.print("\n[bold blue]Thank you for using Automatic Subtitle Generator! 👋[/bold blue]")
                    break
                    
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye! 👋[/yellow]")
            sys.exit(0)
    
    def handle_single_video(self):
        """Handle single video processing workflow"""
        video_file = self.select_single_video()
        
        if not video_file:
            return
        
        # Add to recent files
        self.add_to_recent_files(video_file)
        
        # Show processing summary
        console.clear()
        print_header("🎬 Processing Configuration")
        
        config_table = Table(show_header=False, box=None, padding=(0, 2))
        config_table.add_column("Setting", style="cyan", width=15)
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Video File", os.path.basename(video_file))
        config_table.add_row("Model", self.settings['model'])
        config_table.add_row("Language", self.settings['language'])
        config_table.add_row("Preview", "Yes" if self.settings['preview'] else "No")
        config_table.add_row("Output Dir", self.settings['output_dir'])
        
        console.print(config_table)
        
        if not Confirm.ask("\n[bold cyan]Start processing?[/bold cyan]", default=True):
            return
        
        # Import processing function
        from main import process_single_video
        
        try:
            console.clear()
            srt_file = process_single_video(
                video_file, 
                self.settings['model'], 
                self.settings['language'], 
                self.settings['preview']
            )
            
            print_header("🎉 Processing Complete!")
            print_success(f"SRT file saved: {srt_file}")
            
            console.input("\nPress Enter to continue...")
            
        except Exception as e:
            print_error(f"Processing failed: {e}")
            console.input("\nPress Enter to continue...")
    
    def handle_batch_processing(self):
        """Handle batch processing workflow"""
        console.clear()
        print_header("📁 Batch Processing Setup")
        
        # Get source selection
        source_options = [
            ("1", "📂 Directory", "Process all videos in a directory"),
            ("2", "🔍 Pattern", "Use glob pattern (*.mp4, etc.)"),
            ("3", "✏️  Manual list", "Enter multiple file paths"),
            ("b", "⬅️  Back", "Return to main menu")
        ]
        
        self.show_menu_table(source_options)
        
        choice = Prompt.ask(
            "\n[bold cyan]How to select videos?[/bold cyan]",
            choices=["1", "2", "3", "b"],
            default="1"
        )
        
        if choice == "b":
            return
        
        video_files = []
        
        if choice == "1":
            directory = self.select_directory()
            if directory:
                recursive = Confirm.ask("Search subdirectories recursively?", default=False)
                video_files = self.batch_processor.find_video_files([directory], recursive)
        
        elif choice == "2":
            pattern = Prompt.ask("Enter glob pattern", default="*.mp4")
            video_files = self.batch_processor.find_video_files([pattern], False)
        
        elif choice == "3":
            video_files = self.enter_multiple_files()
        
        if not video_files:
            print_info("No video files found.")
            console.input("Press Enter to continue...")
            return
        
        # Show batch summary and confirm
        if not self.batch_processor.confirm_batch_processing(video_files):
            return
        
        # Process batch
        from main import process_single_video
        
        def batch_process_func(video_file):
            return process_single_video(
                video_file, 
                self.settings['model'], 
                self.settings['language'], 
                self.settings['preview']
            )
        
        results = self.batch_processor.process_batch(video_files, batch_process_func)
        self.batch_processor.show_batch_results()
        
        console.input("\nPress Enter to continue...")
    
    def select_directory(self) -> Optional[str]:
        """Directory selection"""
        directory = Prompt.ask(
            "Enter directory path",
            default="."
        )
        
        directory = os.path.expanduser(directory)
        
        if not os.path.exists(directory):
            print_error(f"Directory not found: {directory}")
            return None
        
        if not os.path.isdir(directory):
            print_error(f"Path is not a directory: {directory}")
            return None
        
        return directory
    
    def enter_multiple_files(self) -> List[str]:
        """Enter multiple file paths"""
        console.print("\n[bold cyan]Enter video file paths (one per line, empty line to finish):[/bold cyan]")
        
        files = []
        while True:
            file_path = Prompt.ask(f"File {len(files) + 1}", default="")
            
            if not file_path:
                break
            
            file_path = os.path.expanduser(file_path)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                files.append(file_path)
                print_success(f"Added: {os.path.basename(file_path)}")
            else:
                print_error(f"File not found: {file_path}")
        
        return files
    
    def show_recent_files(self):
        """Show recent files menu"""
        console.clear()
        print_header("📊 Recent Files")
        
        if not self.recent_files:
            console.print("[yellow]No recent files found.[/yellow]")
            console.input("\nPress Enter to continue...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("File", style="cyan")
        table.add_column("Directory", style="dim")
        table.add_column("Status", style="white", width=8)
        
        for i, file_path in enumerate(self.recent_files, 1):
            filename = os.path.basename(file_path)
            directory = os.path.dirname(file_path)
            status = "✅ Exists" if os.path.exists(file_path) else "❌ Missing"
            
            table.add_row(str(i), filename, directory, status)
        
        console.print(table)
        console.input("\nPress Enter to continue...")