from typing import List, Optional
from .file_system import FileSystemItem
from .file_system_formatter import FileSystemFormatter, NameFormatter
from .file_system_filter import FileSystemFilter, HiddenItemsFilter

class FileSystemProcessor:
    """Orchestrates the processing of filesystem items"""
    def __init__(self,
                 filters: Optional[List[FileSystemFilter]] = None, 
                 formatter: Optional[FileSystemFormatter] = None):
        self.filters = filters or []
        self.formatter = formatter or NameFormatter()

    def process(self, items: List[FileSystemItem]) -> List[str]:
        """
        Process items through filters, sorters, and formatter
        
        :param items: List of filesystem items
        :return: Formatted list of items
        """
        # Apply filters
        for filter_obj in self.filters:
            items = filter_obj.filter(items)
        
        # Format and return
        return self.formatter.format(items)
