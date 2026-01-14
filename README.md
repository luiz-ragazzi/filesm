# File Manager

A Python utility to read and delete files in a folder with optional date range filtering.

## Features

- Read files from a specified folder
- Filter files by modification date range
- Delete files with optional confirmation prompt
- Command-line interface for easy usage

## Installation

No external dependencies required. Uses only Python standard library.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Command Line

Delete all files in a folder:
```bash
python read_files.py -p "files"
```

Delete files from a specific date range:
```bash
python read_files.py -p "files" -s 2026-01-01 -e 2026-01-14
```

Delete without confirmation prompt:
```bash
python read_files.py -p "files" --no-confirm
```

View help:
```bash
python read_files.py --help
```

### In Python

```python
from read_files import delete_files, read_files_in_folder
from datetime import datetime

# Read files
files = read_files_in_folder("files")

# Delete files with date filtering
deleted_count, deleted_files = delete_files(
    folder_path="files",
    start_date=datetime(2026, 1, 1),
    end_date=datetime(2026, 1, 14),
    confirm=True
)
```

## Arguments

- `-p, --path`: Folder path to process (default: current folder)
- `-s, --start-date`: Start date for filtering (format: YYYY-MM-DD)
- `-e, --end-date`: End date for filtering (format: YYYY-MM-DD)
- `--no-confirm`: Skip confirmation prompt before deleting

## License

MIT
