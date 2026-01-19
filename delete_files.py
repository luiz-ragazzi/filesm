import os
from pathlib import Path
from datetime import datetime
import argparse


def read_files_in_folder(folder_path=".", start_date=None, end_date=None, recursive=False):
    """
    Read and list all files in the specified folder, optionally filtered by date range.
    Excludes picture files (jpg, jpeg, png, gif, bmp, webp, svg, tiff, ico).
    
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
        recursive (bool): If True, search in subfolders. Defaults to False.
    
    Returns:
        list: List of tuples (full_path, file_name) for files matching the date criteria, excluding pictures.
    """
    picture_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico'}
    try:
        files = []
        if recursive:
            for root, dirs, filenames in os.walk(folder_path):
                for f in filenames:
                    file_path = os.path.join(root, f)
                    # Skip picture files
                    if Path(f).suffix.lower() in picture_extensions:
                        continue
                    if start_date or end_date:
                        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if start_date and mod_time < start_date:
                            continue
                        if end_date and mod_time > end_date:
                            continue
                    files.append((file_path, f))
        else:
            for f in os.listdir(folder_path):
                file_path = os.path.join(folder_path, f)
                if os.path.isfile(file_path):
                    # Skip picture files
                    if Path(f).suffix.lower() in picture_extensions:
                        continue
                    if start_date or end_date:
                        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if start_date and mod_time < start_date:
                            continue
                        if end_date and mod_time > end_date:
                            continue
                    files.append((file_path, f))
        return files
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []


def read_files_in_folder_pathlib(folder_path=".", start_date=None, end_date=None, recursive=False):
    """
    Read and list all files in the specified folder using pathlib, optionally filtered by date range.
    Excludes picture files (jpg, jpeg, png, gif, bmp, webp, svg, tiff, ico).
      
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
        recursive (bool): If True, search in subfolders. Defaults to False.
    
    Returns:
        list: List of file names in the folder matching the date criteria, excluding pictures.
    """
    picture_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico'}
    try:
        path = Path(folder_path)
        files = []
        pattern = "**/*" if recursive else "*"
        for f in path.glob(pattern):
            if f.is_file():
                # Skip picture files
                if f.suffix.lower() in picture_extensions:
                    continue
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


def delete_files(folder_path=".", start_date=None, end_date=None, confirm=True, recursive=False):
    """
    Read files in a folder and delete them, optionally filtered by date range.
    
    Args:
        folder_path (str): Path to the folder. Defaults to current folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
        confirm (bool): If True, ask for confirmation before deleting. Defaults to True.
        recursive (bool): If True, search in subfolders. Defaults to False.
    
    Returns:
        tuple: (number of deleted files, list of file names deleted)
    """
    try:
        # Get list of files to delete
        files_to_delete = read_files_in_folder(folder_path, start_date, end_date, recursive)
        
        if not files_to_delete:
            print("No files found to delete.")
            return 0, []
        
        # Show files to be deleted
        print(f"Files to be deleted ({len(files_to_delete)}):")
        for file_path, file_name in files_to_delete:
            print(f"  - {file_path}")
        
        # Ask for confirmation
        if confirm:
            response = input(f"\nAre you sure you want to delete these files? Total files: {len(files_to_delete)} (yes/no): ")
            if response.lower() != "yes":
                print("Deletion cancelled.")
                return 0, []
        
        # Delete files
        deleted_count = 0
        deleted_files = []
        for file_path, file_name in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
                deleted_files.append(file_name)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
        
        print(f"\nTotal files found: {len(files_to_delete)}")
        print(f"Successfully deleted {deleted_count} file(s).")
        return deleted_count, deleted_files
    
    except Exception as e:
        print(f"Error during deletion: {e}")
        return 0, []


def move_files_by_type(source_folder=".", file_type="", destination_folder=".", start_date=None, end_date=None, confirm=True, recursive=False):
    """
    Move files of a specific type to a destination folder, optionally filtered by date range.
    
    Args:
        source_folder (str): Path to the source folder. Defaults to current folder.
        file_type (str): File extension or type to move (e.g., ".pdf", ".txt"). If empty, moves all files.
        destination_folder (str): Path to the destination folder.
        start_date (datetime): Start date for filtering. If None, no lower bound.
        end_date (datetime): End date for filtering. If None, no upper bound.
        confirm (bool): If True, ask for confirmation before moving. Defaults to True.
        recursive (bool): If True, search in subfolders. Defaults to False.
    
    Returns:
        tuple: (number of moved files, list of file names moved)
    """
    import shutil
    
    try:
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created destination folder: {destination_folder}")
        
        # Normalize file_type to include dot if not present
        if file_type and not file_type.startswith("."):
            file_type = "." + file_type
        
        # Get list of files
        all_files = read_files_in_folder(source_folder, start_date, end_date, recursive)
        
        # Filter by file type
        files_to_move = []
        for file_path, file_name in all_files:
            if not file_type or Path(file_name).suffix.lower() == file_type.lower():
                files_to_move.append((file_path, file_name))
        
        if not files_to_move:
            print(f"No files found with type '{file_type}' to move.")
            return 0, []
        
        # Show files to be moved
        print(f"Files to be moved ({len(files_to_move)}):")
        for file_path, file_name in files_to_move:
            print(f"  - {file_path}")
        
        # Ask for confirmation
        if confirm:
            response = input(f"\nAre you sure you want to move these files? Total files: {len(files_to_move)} (yes/no): ")
            if response.lower() != "yes":
                print("Move cancelled.")
                return 0, []
        
        # Move files
        moved_count = 0
        moved_files = []
        for file_path, file_name in files_to_move:
            try:
                destination_path = os.path.join(destination_folder, file_name)
                shutil.move(file_path, destination_path)
                moved_count += 1
                moved_files.append(file_name)
                print(f"Moved: {file_path} -> {destination_path}")
            except Exception as e:
                print(f"Failed to move {file_path}: {e}")
        
        print(f"\nTotal files found: {len(files_to_move)}")
        print(f"Successfully moved {moved_count} file(s).")
        return moved_count, moved_files
    
    except Exception as e:
        print(f"Error during move: {e}")
        return 0, []


def move_files_by_year(source_folder=".", destination_folder=None, confirm=True, recursive=False):
    """
    Move files to year-based folders based on their modification date.
    Creates folders named with the year (e.g., 2025, 2026) and organizes files accordingly.
    
    Args:
        source_folder (str): Path to the source folder. Defaults to current folder.
        destination_folder (str): Base path where year folders will be created. If None, uses source_folder.
        confirm (bool): If True, ask for confirmation before moving. Defaults to True.
        recursive (bool): If True, search in subfolders. Defaults to False.
    
    Returns:
        tuple: (number of moved files, dict with year as key and list of moved file names as value)
    """
    import shutil
    
    try:
        # Use source folder as destination if not specified
        if destination_folder is None:
            destination_folder = source_folder
        
        # Get list of all files
        all_files = read_files_in_folder(source_folder, recursive=recursive)
        
        if not all_files:
            print("No files found to move.")
            return 0, {}
        
        # Organize files by year
        files_by_year = {}
        for file_path, file_name in all_files:
            try:
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                year = str(mod_time.year)
                if year not in files_by_year:
                    files_by_year[year] = []
                files_by_year[year].append((file_path, file_name))
            except Exception as e:
                print(f"Warning: Could not get modification date for {file_path}: {e}")
        
        # Show files to be moved
        print(f"Files to be moved by year ({len(all_files)} total):")
        for year in sorted(files_by_year.keys()):
            print(f"  {year}: {len(files_by_year[year])} file(s)")
            for file_path, file_name in files_by_year[year]:
                print(f"    - {file_path}")
        
        # Ask for confirmation
        if confirm:
            response = input(f"\nAre you sure you want to move these files? Total files: {len(all_files)} (yes/no): ")
            if response.lower() != "yes":
                print("Move cancelled.")
                return 0, {}
        
        # Create year folders and move files
        moved_count = 0
        moved_files = {}
        
        for year, files in files_by_year.items():
            year_folder = os.path.join(destination_folder, year)
            
            # Create year folder if it doesn't exist
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)
                print(f"Created folder: {year_folder}")
            
            moved_files[year] = []
            
            # Move files to year folder
            for file_path, file_name in files:
                try:
                    destination_path = os.path.join(year_folder, file_name)
                    shutil.move(file_path, destination_path)
                    moved_count += 1
                    moved_files[year].append(file_name)
                    print(f"Moved: {file_path} -> {destination_path}")
                except Exception as e:
                    print(f"Failed to move {file_path}: {e}")
        
        print(f"\nTotal files found: {len(all_files)}")
        print(f"Successfully moved {moved_count} file(s).")
        return moved_count, moved_files
    
    except Exception as e:
        print(f"Error during move: {e}")
        return 0, {}


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
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search in subfolders recursively"
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
        confirm=confirm,
        recursive=args.recursive
    )


if __name__ == "__main__":
    main()
