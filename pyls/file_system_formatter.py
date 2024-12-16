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
