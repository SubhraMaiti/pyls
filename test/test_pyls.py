import pytest
from typing import Dict, Any
import json
from pathlib import Path
import tempfile
import os

from pyls.file_system_loader import FileSystemLoader
from pyls.file_system_formatter import NameFormatter, DetailedFormatter
from pyls.file_system_filter import HiddenItemsFilter, TypeFilter
from pyls.file_system_sorter import ReverseSorter, TimeSorter

@pytest.fixture
def sample_filesystem_json() -> Dict[str, Any]:
    """Create a sample filesystem structure for testing"""
    return {
        "name": "interpreter",
        "size": 4096,
        "time_modified": 1699957865,
        "permissions": "-rw-r--r--",
        "contents": [
            {
            "name": ".gitignore",
            "size": 8911,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
            },
            {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
            },
            {
            "name": "README.md",
            "size": 83,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
            },
            {
            "name": "ast",
            "size": 4096,
            "time_modified": 1699957739,
            "permissions": "-rw-r--r--",
            "contents": [
                {
                "name": "go.mod",
                "size": 225,
                "time_modified": 1699957780,
                "permissions": "-rw-r--r--"
                },
                {
                "name": "ast.go",
                "size": 837,
                "time_modified": 1699957719,
                "permissions": "drwxr-xr-x"
                }
            ]
            },
            {
            "name": "go.mod",
            "size": 60,
            "time_modified": 1699950073,
            "permissions": "drwxr-xr-x"
            },
            {
            "name": "lexer",
            "size": 4096,
            "time_modified": 1699955487,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                "name": "lexer_test.go",
                "size": 1729,
                "time_modified": 1699955126,
                "permissions": "drwxr-xr-x"
                },
                {
                "name": "go.mod",
                "size": 227,
                "time_modified": 1699944819,
                "permissions": "-rw-r--r--"
                },
                {
                "name": "lexer.go",
                "size": 2886,
                "time_modified": 1699955487,
                "permissions": "drwxr-xr-x"
                }
            ]
            },
            {
            "name": "main.go",
            "size": 74,
            "time_modified": 1699950453,
            "permissions": "-rw-r--r--"
            },
            {
            "name": "parser",
            "size": 4096,
            "time_modified": 1700205662,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                "name": "parser_test.go",
                "size": 1342,
                "time_modified": 1700205662,
                "permissions": "drwxr-xr-x"
                },
                {
                "name": "parser.go",
                "size": 1622,
                "time_modified": 1700202950,
                "permissions": "-rw-r--r--"
                },
                {
                "name": "go.mod",
                "size": 533,
                "time_modified": 1699958000,
                "permissions": "drwxr-xr-x"
                }
            ]
            },
            {
            "name": "token",
            "size": 4096,
            "time_modified": 1699954070,
            "permissions": "-rw-r--r--",
            "contents": [
                {
                "name": "token.go",
                "size": 910,
                "time_modified": 1699954070,
                "permissions": "-rw-r--r--"
                },
                {
                "name": "go.mod",
                "size": 66,
                "time_modified": 1699944730,
                "permissions": "drwxr-xr-x"
                }
            ]
            }
        ]
    }

@pytest.fixture
def temp_json_file(sample_filesystem_json):
    """Create a temporary JSON file with sample filesystem"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        json.dump(sample_filesystem_json, temp_file)
        temp_file_path = temp_file.name
    
    yield Path(temp_file_path)
    
    # Cleanup
    os.unlink(temp_file_path)

def test_filesystem_loader(temp_json_file, sample_filesystem_json):
    """Test loading filesystem from JSON"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    
    assert root.name == "interpreter"
    assert len(root.contents) == 9
    assert any(item.name == ".gitignore" for item in root.contents)
    assert any(item.name == "lexer" for item in root.contents)

def test_filesystem_formatters(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    # Test name formatter
    name_formatter = NameFormatter()
    names = name_formatter.format(items)
    assert names == ['.gitignore', 'LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']

def test_filesystem_filters(temp_json_file):
    """Test filesystem filtering"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    # Test hidden items filter
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    assert not any(item.name.startswith('.') for item in filtered_items)

def test_filesystem_show_all_items(temp_json_file):
    """Test filesystem filtering"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    # Test hidden items filter
    hidden_filter = HiddenItemsFilter(show_hidden=True)
    filtered_items = hidden_filter.filter(items)
    name_formatter = NameFormatter()
    names = name_formatter.format(filtered_items)
    assert names == ['.gitignore', 'LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']

def test_detailed_formatters(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    #filter hidden items
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    
    # Test name formatter
    name_formatter = DetailedFormatter()
    names = name_formatter.format(filtered_items)
    assert names == [
                        'drwxr-xr-x 1071 Nov 14 11:27 LICENSE',
                        'drwxr-xr-x   83 Nov 14 11:27 README.md',
                        '-rw-r--r-- 4096 Nov 14 15:58 ast',
                        'drwxr-xr-x   60 Nov 14 13:51 go.mod',
                        'drwxr-xr-x 4096 Nov 14 15:21 lexer',
                        '-rw-r--r--   74 Nov 14 13:57 main.go',
                        'drwxr-xr-x 4096 Nov 17 12:51 parser',
                        '-rw-r--r-- 4096 Nov 14 14:57 token'
                    ]
    
def test_reverse_sorter(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    #filter hidden items
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    
    #sort in reverse direction
    reverse_sorter = ReverseSorter()
    sorted_items = reverse_sorter.sort(filtered_items)

    # Test name formatter
    name_formatter = DetailedFormatter()
    names = name_formatter.format(sorted_items)
    assert names == [
                        '-rw-r--r-- 4096 Nov 14 14:57 token',
                        'drwxr-xr-x 4096 Nov 17 12:51 parser',
                        '-rw-r--r--   74 Nov 14 13:57 main.go',
                        'drwxr-xr-x 4096 Nov 14 15:21 lexer',
                        'drwxr-xr-x   60 Nov 14 13:51 go.mod',
                        '-rw-r--r-- 4096 Nov 14 15:58 ast',
                        'drwxr-xr-x   83 Nov 14 11:27 README.md',
                        'drwxr-xr-x 1071 Nov 14 11:27 LICENSE'                       
                    ]
    
def test_time_sorter(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    #filter hidden items
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    
    #sort in reverse direction
    reverse_sorter = TimeSorter()
    sorted_items = reverse_sorter.sort(filtered_items)

    # Test name formatter
    name_formatter = DetailedFormatter()
    names = name_formatter.format(sorted_items)
    assert names == [
                        'drwxr-xr-x 1071 Nov 14 11:27 LICENSE',
                        'drwxr-xr-x   83 Nov 14 11:27 README.md',
                        'drwxr-xr-x   60 Nov 14 13:51 go.mod',
                        '-rw-r--r--   74 Nov 14 13:57 main.go',
                        '-rw-r--r-- 4096 Nov 14 14:57 token',
                        'drwxr-xr-x 4096 Nov 14 15:21 lexer',
                        '-rw-r--r-- 4096 Nov 14 15:58 ast',
                        'drwxr-xr-x 4096 Nov 17 12:51 parser'                          
                    ]
    
def test_dir_filter(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    #filter hidden items
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    type_filter = TypeFilter("dir")
    filtered_items = type_filter.filter(filtered_items)

    #sort in reverse direction
    reverse_sorter = TimeSorter()
    sorted_items = reverse_sorter.sort(filtered_items)

    # Test name formatter
    name_formatter = DetailedFormatter()
    names = name_formatter.format(sorted_items)
    assert names == [
                        '-rw-r--r-- 4096 Nov 14 14:57 token',
                        'drwxr-xr-x 4096 Nov 14 15:21 lexer',
                        '-rw-r--r-- 4096 Nov 14 15:58 ast',
                        'drwxr-xr-x 4096 Nov 17 12:51 parser'                          
                    ]

def test_file_filter(temp_json_file):
    """Test filesystem formatters"""
    root = FileSystemLoader.load_from_json(temp_json_file)
    items = root.contents

    #filter hidden items
    hidden_filter = HiddenItemsFilter(show_hidden=False)
    filtered_items = hidden_filter.filter(items)
    type_filter = TypeFilter("file")
    filtered_items = type_filter.filter(filtered_items)

    #sort in reverse direction
    reverse_sorter = TimeSorter()
    sorted_items = reverse_sorter.sort(filtered_items)

    # Test name formatter
    name_formatter = DetailedFormatter()
    names = name_formatter.format(sorted_items)
    assert names == [
                        'drwxr-xr-x 1071 Nov 14 11:27 LICENSE',
                        'drwxr-xr-x   83 Nov 14 11:27 README.md',
                        'drwxr-xr-x   60 Nov 14 13:51 go.mod',
                        '-rw-r--r--   74 Nov 14 13:57 main.go'
                    ]