from typing import Union, Optional
from .file_system import File, Directory
from .file_system_error import FileSystemError

class FileSystemNavigator:
    """Responsible for navigating the filesystem"""
    @staticmethod
    def navigate(root: Union[File, Directory], path: Optional[str] = None) -> Union[File, Directory]:
        """
        Navigate to a specific path in the filesystem
        
        :param root: Root directory or file
        :param path: Path to navigate to
        :return: File or Directory at the specified path
        """
        if not path or path in ['.', './']:
            return root
        
        # Remove leading ./ if present
        path = path.lstrip('./')
        
        # If it's a directory
        if isinstance(root, Directory):
            for item in root.contents:
                if item.name == path:
                    return item
            
            # If path represents a nested directory or file
            if '/' in path:
                current_path = path.split('/')[0]
                remaining_path = '/'.join(path.split('/')[1:])
                
                for item in root.contents:
                    if item.name == current_path and item.is_directory():
                        return FileSystemNavigator.navigate(item, remaining_path)
        
        raise FileSystemError(f"Cannot access '{path}': No such file or directory")