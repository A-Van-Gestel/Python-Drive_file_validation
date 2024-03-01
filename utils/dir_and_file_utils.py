import os
from os import listdir
from os.path import isdir, isfile, join, basename, normpath


def read_file_to_list(file_path: str) -> list[str]:
    f = open(file_path, mode='r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    return [line.rstrip('\n') for line in lines]


def read_file_to_string(file_path: str) -> str:
    f = open(file_path, mode='r', encoding='utf-8')
    lines = f.read()
    f.close()
    return lines


def write_string_to_file(file_path: str, contents: str) -> None:
    f = open(file_path, 'w', encoding='utf-8')
    f.write(contents)
    f.close()


def read_or_create_file(file_path):
    _contents: list[str] = []
    if os.path.isfile(file_path):
        _contents = read_file_to_list(file_path)
    else:
        write_string_to_file(file_path, '\n'.join(_contents))
    # Remove empty strings
    _contents = [i for i in _contents if i]
    return _contents


def list_directory(directory_path: str) -> tuple[list[str], list[str]]:
    """
    Get all the directories & files_list in a given directory with file paths.
    :param directory_path: Path to a directory.
    :return: Tuple of directories & files_list.
    """
    directory_path = normpath(directory_path)
    directories = []
    files = []

    if isdir(directory_path):
        try:
            for item in listdir(directory_path):
                item_path = join(directory_path, item)

                # Add directories
                if isdir(item_path):
                    directories.append(item)
                # Add files_list
                elif isfile(item_path):
                    files.append(item_path)
        except PermissionError:
            return directories, files

    return directories, files


def recursive_list_directory(directory_path: str, parent: str = None, dictionary: dict = None) -> dict[str, list[str]]:
    """
    Get all the directories & files_list in a given directory, including subdirectories with file paths.
    :param directory_path: Path to a directory.
    :param parent: Parent folder name
    :param dictionary: Dictionary to append to
    :return: Flat dictionary[relative folder name, list of files_list]
    """
    directory_path = normpath(directory_path)
    dictionary = {} if dictionary is None else dictionary
    directories, files = list_directory(directory_path)
    folder_name = basename(directory_path)

    if parent is not None:
        folder_name = f"{parent}/{folder_name}"

    dictionary[folder_name] = files
    for directory in directories:
        dictionary.update(recursive_list_directory(join(directory_path, directory), folder_name, dictionary))

    return dictionary
