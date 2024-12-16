from typing import List, Optional
from .file_system import FileSystemItem
from .file_system_formatter import FileSystemFormatter, NameFormatter

class FileSystemProcessor:
    """Orchestrates the processing of filesystem items"""
    def __init__(self, 
                 formatter: Optional[FileSystemFormatter] = None):
        self.formatter = formatter or NameFormatter()

    def process(self, items: List[FileSystemItem]) -> List[str]:
        """
        Process items through filters, sorters, and formatter
        
        :param items: List of filesystem items
        :return: Formatted list of items
        """
        # Format and return
        return self.formatter.format(items)
