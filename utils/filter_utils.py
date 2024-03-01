def file_contains_substring(file_path: str, substring: str, window_size: int = 5120) -> bool:
    """
    Check if given file contains the given substring.
    :param file_path: Path to the file to validate.
    :param substring: String that will be checked if it occurs in the given file.
    :param window_size: Number indicating how many bytes will be read in each window.
    :return: Bool: True if file contains given substring, otherwise False.
    """

    validation_string = substring.encode('utf-8')
    with open(file_path, mode='rb') as f:
        prev_data: bytes = b""
        while True:
            data: bytes = f.read(window_size)
            # Stop while loop if reached end of file.
            if not data:
                break
            # Check on concatenation of last and current data windows, as it might be possible that the string would be cut off between two windows.
            if (prev_data + data).find(validation_string) >= 0:
                return True
            prev_data = data
        return False
