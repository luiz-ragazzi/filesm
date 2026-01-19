from delete_files import move_files_by_year
import argparse
from datetime import datetime


def main():
    """
    Command-line interface for moving files by year.
    """
    parser = argparse.ArgumentParser(
        description="Move files to year-based folders based on their modification date.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python move_files.py -s files
  python move_files.py -s files -d /path/to/destination
  python move_files.py -s files -r
  python move_files.py -s files --no-confirm -r
        """
    )
    
    parser.add_argument(
        "-s", "--source",
        default=".",
        help="Source folder path (default: current folder)"
    )
    parser.add_argument(
        "-d", "--destination",
        default=None,
        help="Destination base folder for year subfolders (default: same as source folder)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search in subfolders recursively"
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip confirmation prompt before moving"
    )
    
    args = parser.parse_args()
    
    # Call move_files_by_year with parsed arguments
    confirm = not args.no_confirm
    moved_count, files_by_year = move_files_by_year(
        source_folder=args.source,
        destination_folder=args.destination,
        confirm=confirm,
        recursive=args.recursive
    )
    
    print(f"\nMoved {moved_count} files")
    if files_by_year:
        print("Organization by year:")
        for year in sorted(files_by_year.keys()):
            print(f"  {year}: {len(files_by_year[year])} file(s)")


if __name__ == "__main__":
    main()

