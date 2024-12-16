from abc import ABC, abstractmethod
from typing import List

from .file_system import FileSystemItem

class FileSystemSorter(ABC):
    """Abstract base class for sorting filesystem items"""
    @abstractmethod
    def sort(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        """Sort the given items"""
        pass

class ReverseSorter(FileSystemSorter):
    """Sort items in reverse direction"""
    def sort(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        return reversed(items)
    
class TimeSorter(FileSystemSorter):
    """Sort items by modification time"""
    def sort(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        return sorted(items, key=lambda x: x.time_modified)