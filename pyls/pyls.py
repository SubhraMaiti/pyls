from pathlib import Path
import argparse
import sys

from typing import Optional, List

from .file_system_loader import FileSystemLoader
from .file_system_error import FileSystemError
from .file_system_processor import FileSystemProcessor
from .file_system_formatter import NameFormatter
from .file_system_filter import HiddenItemsFilter

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
                HiddenItemsFilter()
            ]

            # Determine formatter
            formatter = NameFormatter()

            # Create and run processor
            # Create and run processor
            processor = FileSystemProcessor(
                filters=filters, 
                formatter=formatter
            )
            output = processor.process(items)

            # Print output
            if type(formatter) == NameFormatter:
                print(" ".join(output))

        except (FileSystemError, ValueError) as e:
            print(f"error: {e}")
            sys.exit(1)

    
    def _create_argument_parser(self):
        """
        Create argument parser
        
        :return: Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--help', action='store_true', help='Show help message')
        return parser
    
    def _show_help(self):
        """Display help information"""
        help_text = """Usage: python -m pyls [OPTIONS] [PATH]

Examples:
  python -m pyls                  # List files in current directory
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