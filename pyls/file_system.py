from abc import abstractmethod
from typing import List, Union

class FileSystemItem:
    """Base class for file system items"""
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.name = name
        self.size = size
        self.time_modified = time_modified
        self.permissions = permissions

    @abstractmethod
    def is_directory(self) -> bool:
        """Check if the item is a directory"""
        pass

class File(FileSystemItem):
    """Represents a file in the file system"""
    def is_directory(self) -> bool:
        return False

class Directory(FileSystemItem):
    """Represents a directory in the file system"""
    def __init__(self, name: str, size: int, time_modified: int, permissions: str, contents: List[Union[File, 'Directory']]):
        super().__init__(name, size, time_modified, permissions)
        self.contents = contents

    def is_directory(self) -> bool:
        return True