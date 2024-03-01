import os
import shutil
import sys

from utils.date_and_time_utils import get_current_datetime
from utils.dir_and_file_utils import recursive_list_directory, write_string_to_file, read_or_create_file
from utils.filter_utils import file_contains_substring

if __name__ == '__main__':
    source_drive: str = 'G:\\'
    dest_drive: str = 'G:\\!\\'
    files_error_file_location: str = r'.\files_error.txt'
    files_containing_bad_sectors_file_location: str = r'.\files_containing_bad_sectors.txt'
    validated_files_cache_file_location: str = r'.\_cache.txt'

    validation_string: str = 'Read error in the sector !'

    files_error: list[str] = read_or_create_file(files_error_file_location)
    files_moved: list[str] = read_or_create_file(files_containing_bad_sectors_file_location)
    cached_files: list[str] = read_or_create_file(validated_files_cache_file_location)

    print("---------------------------------------------")
    print(f"{get_current_datetime()} | Starting file validation")
    print("---------------------------------------------")
    print(f"Source path: {source_drive}")
    print(f"Destination path: {dest_drive}")
    print(f"String to validate: {validation_string}")
    print("---------------------------------------------")

    print(f"{get_current_datetime()} | Searching for files to validate")
    print("---------------------------------------------")

    recursive_directory_files_dict: dict[str, list[str]] = recursive_list_directory(source_drive)
    file_list: list[str] = [file for files in [files_list for files_list in recursive_directory_files_dict.values() if len(files_list) > 0] for file in files]
    file_list_length: int = len(file_list)

    print(f"Total files found: {file_list_length}")
    print("---------------------------------------------")

    try:
        for index, source_path in enumerate(file_list):
            print(f"{get_current_datetime()} | {(file_list_length - index):,} left | {source_path}")

            # Skip files that are already processed / cached.
            if source_path in cached_files:
                continue

            # Add current file to cache.
            cached_files.append(source_path)
            # write_string_to_file(validated_files_cache_file_location, '\n'.join(cached_files))

            # Skip files in destination folder or that are already processed / cached.
            if source_path.startswith(dest_drive):
                continue

            # Only process files that are in the source folder.
            if source_path.startswith(source_drive):
                dest_path: str = source_path.replace(source_drive, dest_drive, 1)
            else:
                print(f'{get_current_datetime()} | Skipping {source_path}: Not on {source_drive}')
                files_error.append(source_path)
                continue

            # Skip should the file already exist in the destination folder.
            if os.path.exists(dest_path):
                continue

            # Check if the file still exists before attempting to analyze it.
            if not os.path.exists(source_path):
                print(f'{get_current_datetime()} | Skipping {source_path}: File does not exist')
                files_error.append(source_path)
                continue

            # Analyze the file, skip the moving of the file if it is valid.
            if not file_contains_substring(source_path, validation_string):
                cached_files.append(source_path)
                continue

            # Create the nested folder structure of the source path in the destination folder.
            dest_dir = os.path.dirname(dest_path)
            if not os.path.isdir(dest_dir):
                try:
                    os.makedirs(dest_dir)
                except (OSError, IOError) as e:
                    print(f'{get_current_datetime()} | Error making {dest_dir}: {e}')
                    continue

            # Try to move the file to the same location in the destination folder.
            try:
                shutil.move(source_path, dest_path)
                files_moved.append(source_path)
            except (OSError, IOError) as e:
                print(f'{get_current_datetime()} | Error moving {source_path} to {dest_path}: {e}')
                files_error.append(source_path)

    except KeyboardInterrupt:
        print("---------------------------------------------")
        print(f"{get_current_datetime()} | Interrupt detected... Writing current processed files to text files.")
        # Remove last cached file as it might not have finished analyzing.
        if len(cached_files) > 0:
            cached_files.pop(-1)
            write_string_to_file(validated_files_cache_file_location, '\n'.join(cached_files))

        write_string_to_file(files_error_file_location, '\n'.join(files_error))
        write_string_to_file(files_containing_bad_sectors_file_location, '\n'.join(files_moved))
        print("---------------------------------------------")
        print(f"{get_current_datetime()} | File validation - Interrupted")
        print("---------------------------------------------")
        sys.exit(0)

    write_string_to_file(validated_files_cache_file_location, '\n'.join(cached_files))
    write_string_to_file(files_error_file_location, '\n'.join(files_error))
    write_string_to_file(files_containing_bad_sectors_file_location, '\n'.join(files_moved))

    print("---------------------------------------------")
    print(f"{get_current_datetime()} | Moved {len(files_moved)} / {file_list_length} containing bad read sectors, to {dest_drive}")
    print(f"{get_current_datetime()} | {len(files_error)} files couldn't be accessed.")
    print("---------------------------------------------")
    print(f"{get_current_datetime()} | File validation - Finished")
    print("---------------------------------------------")
