from pathlib import Path
import argparse
import sys

from typing import Optional, List

from .file_system_loader import FileSystemLoader
from .file_system_error import FileSystemError
from .file_system_processor import FileSystemProcessor
from .file_system_formatter import NameFormatter, DetailedFormatter
from .file_system_filter import HiddenItemsFilter, TypeFilter
from .file_system_sorter import ReverseSorter, TimeSorter

class PyLSCommandLineInterface:
    """Handles command-line argument parsing and application logic"""
    def __init__(self, json_path: Path):
        self.json_path = json_path

    def run(self, args: Optional[List[str]] = None):
        """
        Run the pyls command
        
        :param args: Optional list of command-line arguments
        """
        # Parse arguments
        parser = self._create_argument_parser()
        parsed_args = parser.parse_args(args)

        # Handle help flag
        if parsed_args.help:
            self._show_help()
            return
        try:
            # Load filesystem
            root = FileSystemLoader.load_from_json(self.json_path)

            # Prepare items to process
            items = root.contents if hasattr(root, 'contents') else [root]

            # Create filters
            filters = [
                HiddenItemsFilter(parsed_args.all_files)
            ]
            if parsed_args.filter:
                filters.append(TypeFilter(parsed_args.filter))


            # Create sorters
            sorters = []
            if parsed_args.time_sort:
                sorters.append(TimeSorter())
            if parsed_args.reverse:
                sorters.append(ReverseSorter())

            # Determine formatter
            formatter = DetailedFormatter() if parsed_args.long_format else NameFormatter()

            # Create and run processor
            # Create and run processor
            processor = FileSystemProcessor(
                filters=filters,
                sorters=sorters, 
                formatter=formatter
            )
            output = processor.process(items)

            # Print output
            if type(formatter) == NameFormatter:
                print(" ".join(output))
            else:
                for line in output:
                    print(line)

        except (FileSystemError, ValueError) as e:
            print(f"error: {e}")
            sys.exit(1)

    
    def _create_argument_parser(self):
        """
        Create argument parser
        
        :return: Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-A', dest='all_files', action='store_true', help='Show all items')
        parser.add_argument('-l', dest='long_format', action='store_true', help='Long format')
        parser.add_argument('-r', dest='reverse', action='store_true', help='Reverse order')
        parser.add_argument('-t', dest='time_sort', action='store_true', help='Sort by time')
        parser.add_argument('--filter', choices=['file', 'dir'], help='Filter by type')
        parser.add_argument('--help', action='store_true', help='Show help message')
        return parser
    
    def _show_help(self):
        """Display help information"""
        help_text = """Usage: python -m pyls [OPTIONS] [PATH]

Options:
  -A          Show all files, folders including hidden items
  -l          Use long listing format
  -r          Reverse order while sorting
  -t          Sort by time modified
  --filter=   Filter items by type: 'file' or 'dir'

Examples:
  python -m pyls                  # List files in current directory
  python -m pyls -A               # List all files and folder in current directory including hidden
  python -m pyls -l               # Long format listing
  python -m pyls -l -r            # Reverse order
  python -m pyls -l -t            # Sort by time
  python -m pyls -l -t -r         # Sort by time in revrese order
  python -m pyls -l --filter=file # Show only files
  python -m pyls -l --filter=dir # Show only directories
"""
        print(help_text)

def main():
    """Main entry point for pyls command"""
    # Default JSON file path (you might want to change this)
    JSON_PATH = Path('structure.json')
    
    # Create and run CLI
    cli = PyLSCommandLineInterface(JSON_PATH)
    cli.run()

if __name__ == '__main__':
    main()