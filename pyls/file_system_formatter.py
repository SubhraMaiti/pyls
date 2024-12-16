from abc import ABC, abstractmethod
from typing import List
from .file_system import FileSystemItem
from datetime import datetime

class FileSystemFormatter(ABC):
    """Abstract base class for formatting filesystem items"""
    @abstractmethod
    def format(self, items: List[FileSystemItem]) -> List[str]:
        """Format the list of items"""
        pass

class NameFormatter(FileSystemFormatter):
    """Formatter that returns just the names of items"""
    def format(self, items: List[FileSystemItem]) -> List[str]:
        return [item.name for item in items]

class DetailedFormatter(FileSystemFormatter):
    """Formatter that provides detailed information about items"""
    def format(self, items: List[FileSystemItem]) -> List[str]:
        return [
            f"{item.permissions} {item.size:>4} "
            f"{datetime.fromtimestamp(item.time_modified).strftime('%b %d %H:%M')} {item.name}"
            for item in items
        ]

class HumanReadableSizeFormatter(FileSystemFormatter):
    """Formatter that converts sizes to human-readable format"""
    def __init__(self, base_formatter: FileSystemFormatter):
        self.base_formatter = base_formatter

    def _humanize_size(self, size: int) -> str:
        """Convert size to human-readable format"""
        units = [('G', 1_073_741_824), ('M', 1_048_576), ('K', 1_024)]
        for unit, divisor in units:
            if size >= divisor:
                return f"{size/divisor:.1f}{unit}"
        return str(size)

    def format(self, items: List[FileSystemItem]) -> List[str]:
        formatted_items = self.base_formatter.format(items)
        
        # If the base formatter is DetailedFormatter, modify size representation
        if isinstance(self.base_formatter, DetailedFormatter):
            return [
                line.replace(str(line.split()[1]), self._humanize_size(int(line.split()[1])))
                for line in formatted_items
            ]
        
        return formatted_items