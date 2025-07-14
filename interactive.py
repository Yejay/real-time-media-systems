#!/usr/bin/env python3
"""
Interactive CLI launcher for the Automatic Subtitle Generator
Run this file to start the interactive menu system
"""
import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_menu import InteractiveCLI
from utils import console, print_error


def main():
    """Main entry point for interactive mode"""
    try:
        # Check if required dependencies are available
        try:
            import whisper
            import rich
            import tqdm
        except ImportError as e:
            print_error(f"Missing required dependency: {e}")
            print_error("Please run: pip install -r requirements.txt")
            sys.exit(1)
        
        # Launch interactive CLI
        cli = InteractiveCLI()
        cli.run()
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        console.print("\n[dim]If this persists, please report the issue.[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()