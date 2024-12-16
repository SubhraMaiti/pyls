# pyls
pyls is a Python implementation of the Linux `ls` command, capable of listing files and directories from a JSON-defined filesystem structure.

## Overview
pyls is a Python implementation of the Linux `ls` command, capable of listing files and directories from a JSON-defined filesystem structure.

## Features
- List files and directories
- Show hidden files with `-A`
- Long format listing with `-l`
- Reverse order sorting with `-r`
- Sort by modification time with `-t`
- Human-readable file sizes with `-h`
- Filter by file or directory type `--filter={file, dir}

## Usage
```bash
# Basic usage
python -m pyls

# Show all files
python -m pyls -A

# Long format listing
python -m pyls -l

# Reverse order
python -m pyls -l -r

# Sort by time
python -m pyls -l -t

# Filter files or directories
python -m pyls -l --filter=file
python -m pyls -l --filter=dir

# Listing of a particualr PATH in long format
python -m pyls -l PATH

# Show help
python -m pyls --help
```

## Requirements
- Python 3.8+
- `structure.json` file in the same directory

## Notes
Ensure your filesystem is defined in a `structure.json` file following the specified JSON structure.