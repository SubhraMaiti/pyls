from pathlib import Path
import json
from typing import Union, Dict, Any
from .FileSystem import File, Directory
from .FileSystemError import FileSystemError

class FileSystemLoader:
    """Responsible for loading filesystem from JSON"""
    @staticmethod
    def load_from_json(json_path: Path) -> Union[File, Directory]:
        """
        Load filesystem structure from a JSON file
        
        :param json_path: Path to the JSON file
        :return: Root Directory or File
        """
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            return FileSystemLoader._convert_to_filesystem(data)
        except FileNotFoundError:
            raise FileSystemError(f"Cannot access '{json_path}': No such file or directory")
        except json.JSONDecodeError:
            raise FileSystemError("Invalid JSON file")

    @staticmethod
    def _convert_to_filesystem(item_dict: Dict[str, Any]) -> Union[File, Directory]:
        """
        Recursively convert dictionary to File or Directory
        
        :param item_dict: Dictionary representation of filesystem item
        :return: File or Directory instance
        """
        if 'contents' in item_dict:
            contents = [FileSystemLoader._convert_to_filesystem(content) for content in item_dict['contents']]
            return Directory(
                name=item_dict['name'],
                size=item_dict['size'],
                time_modified=item_dict['time_modified'],
                permissions=item_dict['permissions'],
                contents=contents
            )
        else:
            return File(
                name=item_dict['name'],
                size=item_dict['size'],
                time_modified=item_dict['time_modified'],
                permissions=item_dict['permissions']
            )