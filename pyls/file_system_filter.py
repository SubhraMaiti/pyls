from .file_system import FileSystemItem
from abc import ABC, abstractmethod
from typing import List

class FileSystemFilter(ABC):
    """Abstract base class for filtering filesystem items"""
    @abstractmethod
    def filter(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        """Filter the list of items"""
        pass

class HiddenItemsFilter(FileSystemFilter):
    """Filter out hidden items"""
    def __init__(self, show_hidden: bool = False):
        self.show_hidden = show_hidden

    def filter(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        if self.show_hidden:
            return items
        return [item for item in items if not item.name.startswith('.')]