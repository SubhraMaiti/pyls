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

class TypeFilter(FileSystemFilter):
    """Filter items by type (file or directory)"""
    def __init__(self, item_type: str):
        if item_type not in ['file', 'dir']:
            raise ValueError("Type must be 'file' or 'dir'")
        self.item_type = item_type

    def filter(self, items: List[FileSystemItem]) -> List[FileSystemItem]:
        if self.item_type == 'file':
            return [item for item in items if not item.is_directory()]
        return [item for item in items if item.is_directory()]