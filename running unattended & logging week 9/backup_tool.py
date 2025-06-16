import os
import shutil
import argparse
import logging

def setup_logging(log_file, verbose):
    """Set up logging to file with appropriate level and format."""
    log_level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def backup_files(source, destination, verbose):
    """Copy all files from source to destination, logging errors and optionally successes."""
    for filename in os.listdir(source):
        src_path = os.path.join(source, filename)
        dst_path = os.path.join(destination, filename)
        try:
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                if verbose:
                    logging.info(f"Source: {src_path}, Destination: {dst_path}, SUCCESSFULLY COPIED")
        except Exception as e:
            logging.error(f"Source: {src_path}, Destination: {dst_path}, Reason: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Backup files from source to destination directory.")
    parser.add_argument("-s", "--source", required=True, help="Source directory")
    parser.add_argument("-d", "--destination", required=True, help="Destination directory")
    parser.add_argument("-l", "--log", default="backup.log", help="Log file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log successful copies")
    args = parser.parse_args()

    setup_logging(args.log, args.verbose)
    backup_files(args.source, args.destination, args.verbose)

if __name__ == "__main__":
    main()
