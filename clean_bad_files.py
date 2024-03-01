from utils.dir_and_file_utils import read_file_to_list, write_string_to_file


def contains_character(line: str, character: str) -> bool:
    return line.find(character) >= 0


if __name__ == '__main__':
    raw_location: str = r'.\54618_Badfiles.txt'
    save_location: str = r'.\54618_Badfiles_cleaned.txt'

    lines_raw: list[str] = read_file_to_list(raw_location)

    lines_save: list[str] = [line.replace('D:\\Recovered Data\\', 'G:\\') for line in lines_raw if contains_character(line, '?') is False]

    write_string_to_file(save_location, ''.join(lines_save))
    print(f"Wrote {len(lines_save)} / {len(lines_raw)} (Deleted {len(lines_raw) - len(lines_save)} lines) to {save_location}")
