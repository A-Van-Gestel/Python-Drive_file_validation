import os
import re
import shutil
import sys
from re import Match, Pattern
from typing import Iterator

from utils.dir_and_file_utils import read_file_to_string, write_string_to_file
from utils.filter_utils import file_contains_substring


def regex_search(lines: str, regex):
    match: Iterator[Match[str]] = re.finditer(regex, lines)
    return [value['path'] for value in match if value['path'] is not None]


if __name__ == '__main__':
    source_drive: str = 'G:\\'
    dest_drive: str = 'G:\\!\\'
    input_file_location: str = r'.\54618_Badfiles_cleaned.txt'
    files_not_moved_file_location: str = r'.\54618_Badfiles_not_moved.txt'
    files_good_file_location: str = r'.\54618_Badfiles_good.txt'

    regex_path: Pattern[str] = re.compile(r"^.*(?P<path>G:\\.*?)(?: \(\d*\))?$", re.MULTILINE)  # https://regex101.com/r/vhRNSV/1
    raw_file: str = read_file_to_string(input_file_location)
    file_list: list[str] = regex_search(raw_file, regex_path)
    files_not_moved: list[str] = []
    good_files: list[str] = []

    for source_path in file_list:
        if source_path.startswith(source_drive):
            dest_path: str = source_path.replace(source_drive, dest_drive, 1)
        else:
            print(f'Skipping {source_path}: Not on {source_drive}', file=sys.stderr)
            files_not_moved.append(source_path)
            continue

        dest_dir: str = os.path.dirname(dest_path)

        if os.path.exists(dest_path):
            continue

        if not os.path.exists(source_path):
            print(f'Skipping {source_path}: File does not exist', file=sys.stderr)
            files_not_moved.append(source_path)
            continue

        if not file_contains_substring(source_path, 'Read error in the sector !'):
            good_files.append(source_path)
            continue

        if not os.path.isdir(dest_dir):
            try:
                os.makedirs(dest_dir)
            except (OSError, IOError) as e:
                print(f'Error making {dest_dir}: {e}', file=sys.stderr)
                continue

        try:
            shutil.move(source_path, dest_path)
        except (OSError, IOError) as e:
            print(f'Error moving {source_path} to {dest_path}: {e}', file=sys.stderr)
            files_not_moved.append(source_path)

    write_string_to_file(files_not_moved_file_location, '\n'.join(files_not_moved))
    write_string_to_file(files_good_file_location, '\n'.join(good_files))

    print(f"Moved files {len(file_list) - len(files_not_moved)} / {len(file_list)}, ({len(files_not_moved)} not moved) to {dest_drive}")
    print(f"{len(good_files)} files don't contain read errors.")
