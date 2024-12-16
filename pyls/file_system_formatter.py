from abc import ABC, abstractmethod
from typing import List
from .file_system import FileSystemItem
        
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
