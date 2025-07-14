"""
Batch processing functionality for multiple video files
"""
import os
import glob
from pathlib import Path
from typing import List, Tuple
from rich.table import Table
from rich.progress import Progress, TaskID
from utils import console, print_header, print_success, print_error, print_info, create_progress_bar


class BatchProcessor:
    """Handles batch processing of multiple video files"""
    
    def __init__(self):
        self.supported_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm', '.flv', '.wmv'}
        self.results = []
    
    def find_video_files(self, paths: List[str], recursive: bool = False) -> List[str]:
        """
        Find all video files from given paths
        
        Args:
            paths: List of file paths, directory paths, or glob patterns
            recursive: Whether to search directories recursively
            
        Returns:
            List of video file paths
        """
        video_files = []
        
        for path in paths:
            path = os.path.expanduser(path)  # Expand ~ to home directory
            
            if os.path.isfile(path):
                # Single file
                if Path(path).suffix.lower() in self.supported_extensions:
                    video_files.append(path)
                else:
                    print_info(f"Skipping non-video file: {path}")
            
            elif os.path.isdir(path):
                # Directory
                pattern = "**/*" if recursive else "*"
                for ext in self.supported_extensions:
                    glob_pattern = os.path.join(path, f"{pattern}{ext}")
                    video_files.extend(glob.glob(glob_pattern, recursive=recursive))
            
            elif '*' in path or '?' in path:
                # Glob pattern
                matched_files = glob.glob(path, recursive=recursive)
                for file_path in matched_files:
                    if os.path.isfile(file_path) and Path(file_path).suffix.lower() in self.supported_extensions:
                        video_files.append(file_path)
            
            else:
                print_error(f"Path not found: {path}")
        
        # Remove duplicates and sort
        video_files = sorted(list(set(video_files)))
        return video_files
    
    def estimate_total_time(self, video_files: List[str]) -> str:
        """Estimate total processing time based on file sizes"""
        try:
            total_size = sum(os.path.getsize(f) for f in video_files if os.path.exists(f))
            # Rough estimate: ~1 minute processing per 100MB
            estimated_minutes = total_size / (100 * 1024 * 1024)
            
            if estimated_minutes < 1:
                return "< 1 minute"
            elif estimated_minutes < 60:
                return f"~{int(estimated_minutes)} minutes"
            else:
                hours = int(estimated_minutes // 60)
                minutes = int(estimated_minutes % 60)
                return f"~{hours}h {minutes}m"
        except:
            return "unknown"
    
    def show_batch_summary(self, video_files: List[str]):
        """Display a summary of files to be processed"""
        if not video_files:
            print_error("No video files found!")
            return False
        
        print_header("📁 Batch Processing Summary")
        
        # Create summary table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("File", style="cyan")
        table.add_column("Size", style="yellow", justify="right")
        table.add_column("Directory", style="dim")
        
        total_size = 0
        for i, file_path in enumerate(video_files, 1):
            try:
                size = os.path.getsize(file_path)
                total_size += size
                size_str = self._format_file_size(size)
            except:
                size_str = "unknown"
            
            filename = Path(file_path).name
            directory = str(Path(file_path).parent)
            
            # Truncate long paths
            if len(directory) > 40:
                directory = "..." + directory[-37:]
            
            table.add_row(str(i), filename, size_str, directory)
        
        console.print(table)
        
        # Show summary stats
        estimated_time = self.estimate_total_time(video_files)
        print_info(f"📊 Total files: {len(video_files)}")
        print_info(f"📦 Total size: {self._format_file_size(total_size)}")
        print_info(f"⏱️  Estimated time: {estimated_time}")
        
        return True
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def process_batch(self, video_files: List[str], process_function, **kwargs) -> List[Tuple[str, bool, str]]:
        """
        Process a batch of video files
        
        Args:
            video_files: List of video file paths
            process_function: Function to process each video
            **kwargs: Additional arguments for process_function
            
        Returns:
            List of (file_path, success, message/error) tuples
        """
        if not video_files:
            return []
        
        results = []
        
        with create_progress_bar() as progress:
            batch_task = progress.add_task("Overall Progress", total=len(video_files))
            
            for i, video_file in enumerate(video_files, 1):
                filename = Path(video_file).name
                progress.update(batch_task, description=f"Processing {filename} ({i}/{len(video_files)})")
                
                print_header(f"🎬 Processing File {i}/{len(video_files)}", filename)
                
                try:
                    # Process the video file
                    result = process_function(video_file, **kwargs)
                    results.append((video_file, True, result))
                    print_success(f"✅ Completed: {filename}")
                    
                except Exception as e:
                    error_msg = str(e)
                    results.append((video_file, False, error_msg))
                    print_error(f"❌ Failed: {filename} - {error_msg}")
                
                progress.advance(batch_task)
        
        self.results = results
        return results
    
    def show_batch_results(self):
        """Display final batch processing results"""
        if not self.results:
            return
        
        print_header("📊 Batch Processing Results")
        
        successful = [r for r in self.results if r[1]]
        failed = [r for r in self.results if not r[1]]
        
        # Success summary
        if successful:
            print_success(f"✅ Successfully processed: {len(successful)} files")
            for file_path, _, result in successful:
                filename = Path(file_path).name
                print_info(f"  • {filename} → {result}")
        
        # Failure summary
        if failed:
            console.print()
            print_error(f"❌ Failed to process: {len(failed)} files")
            for file_path, _, error in failed:
                filename = Path(file_path).name
                print_error(f"  • {filename}: {error}")
        
        # Overall stats
        total = len(self.results)
        success_rate = (len(successful) / total * 100) if total > 0 else 0
        
        console.print()
        print_info(f"📈 Success rate: {success_rate:.1f}% ({len(successful)}/{total})")
        
        if failed:
            console.print()
            print_info("💡 For failed files, try:")
            print_info("  • Using a smaller model (--model tiny)")
            print_info("  • Processing files individually")
            print_info("  • Checking if files are corrupted")
    
    def confirm_batch_processing(self, video_files: List[str]) -> bool:
        """Ask user to confirm batch processing"""
        if not self.show_batch_summary(video_files):
            return False
        
        console.print()
        response = console.input("🚀 [bold cyan]Proceed with batch processing? (y/n): [/bold cyan]")
        return response.lower() in ['y', 'yes']