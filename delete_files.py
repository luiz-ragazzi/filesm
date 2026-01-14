import os
from pathlib import Path
from datetime import datetime
import argparse


def read_files_in_folder(folder_path=".", start_date=None, end_date=None):
    """
    Read and list all files in the specified folder, optionally filtered by date range.
    
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
    
    Returns:
        list: List of file names in the folder matching the date criteria.
    """
    try:
        files = []
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                if start_date or end_date:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if start_date and mod_time < start_date:
                        continue
                    if end_date and mod_time > end_date:
                        continue
                files.append(f)
        return files
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []


def read_files_in_folder_pathlib(folder_path=".", start_date=None, end_date=None):
    """
    Read and list all files in the specified folder using pathlib, optionally filtered by date range.
    
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
    
    Returns:
        list: List of file names in the folder matching the date criteria.
    """
    try:
        path = Path(folder_path)
        files = []
        for f in path.iterdir():
            if f.is_file():
                if start_date or end_date:
                    mod_time = datetime.fromtimestamp(f.stat().st_mtime)
                    if start_date and mod_time < start_date:
                        continue
                    if end_date and mod_time > end_date:
                        continue
                files.append(f.name)
        return files
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []


def delete_files(folder_path=".", start_date=None, end_date=None, confirm=True):
    """
    Read files in a folder and delete them, optionally filtered by date range.
    
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
        confirm (bool): If True, ask for confirmation before deleting. Defaults to True.
    
    Returns:
        tuple: (number of deleted files, list of file names deleted)
    """
    try:
        # Get list of files to delete
        files_to_delete = read_files_in_folder(folder_path, start_date, end_date)
        
        if not files_to_delete:
            print("No files found to delete.")
            return 0, []
        
        # Show files to be deleted
        print(f"Files to be deleted ({len(files_to_delete)}):")
        for file in files_to_delete:
            print(f"  - {file}")
        
        # Ask for confirmation
        if confirm:
            response = input("\nAre you sure you want to delete these files? (yes/no): ")
            if response.lower() != "yes":
                print("Deletion cancelled.")
                return 0, []
        
        # Delete files
        deleted_count = 0
        deleted_files = []
        for file in files_to_delete:
            file_path = os.path.join(folder_path, file)
            try:
                os.remove(file_path)
                deleted_count += 1
                deleted_files.append(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
        
        print(f"\nSuccessfully deleted {deleted_count} file(s).")
        return deleted_count, deleted_files
    
    except Exception as e:
        print(f"Error during deletion: {e}")
        return 0, []


def main():
    """
    Command-line interface for deleting files with date filtering.
    """
    parser = argparse.ArgumentParser(
        description="Delete files in a folder, optionally filtered by date range.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python read_files.py -p "files"
  python read_files.py -p "files" -s 2026-01-01 -e 2026-01-14
  python read_files.py -p "files" -s 2026-01-10 --no-confirm
        """
    )
    
    parser.add_argument(
        "-p", "--path",
        default=".",
        help="Folder path to read files from (default: current folder)"
    )
    parser.add_argument(
        "-s", "--start-date",
        help="Start date for filtering (format: YYYY-MM-DD)"
    )
    parser.add_argument(
        "-e", "--end-date",
        help="End date for filtering (format: YYYY-MM-DD)"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip confirmation prompt before deleting"
    )
    
    args = parser.parse_args()
    
    # Parse dates
    start_date = None
    end_date = None
    
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid start date format. Use YYYY-MM-DD")
            return
    
    if args.end_date:
        try:
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid end date format. Use YYYY-MM-DD")
            return
    
    # Call delete_files
    confirm = not args.no_confirm
    deleted_count, deleted_files = delete_files(
        folder_path=args.path,
        start_date=start_date,
        end_date=end_date,
        confirm=confirm
    )


if __name__ == "__main__":
    main()
