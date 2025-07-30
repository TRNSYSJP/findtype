import os
import subprocess
import argparse
import re
import sys


def error_exit(message):
    """
    エラーメッセージを出力し、プログラムを終了する。
    Prints the error message and exits the program.

    Args:
        message (str): 出力するエラーメッセージ / The error message to display.
    """
    print(message)
    sys.exit(1)


# 検索対象フォルダのリスト / List of directories to be searched
directory_path = [
    "C:\\TRNSYS18\\Tess Models\\Examples",
    "C:\\TRNSYS18\\Examples",
    "C:\\TRNSYS18\\TRNLib",
]


def export_tpf_to_dck_files(folder):
    """
    指定フォルダ内の .tpf ファイルを .dck ファイルにエクスポートするためにStudio.exeを実行する。
    Executes Studio.exe within the specified folder to export .tpf files to .dck files.
    既存の .dck ファイルがある場合はスキップされる。
    If a .dck file already exists, that file is skipped.

    Args:
        folder (str): 検索対象のフォルダパス / The path of the folder to search.
    """
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".tpf"):
                tpf_path = os.path.join(dirpath, filename)
                dck_path = os.path.splitext(tpf_path)[0] + ".dck"
                if os.path.exists(dck_path):
                    continue
                print(f"Exporting: {tpf_path}")
                studio_exe = "C:\\TRNSYS18\\Studio\\Exe\\Studio.exe"
                subprocess.run([studio_exe, "/d", "/q", tpf_path])


def contains_target_type(dck_file, type_no):
    """
    指定された .dck ファイル内に求める TYPE 番号が存在するかを判定する。
    Checks if the specified .dck file contains the target TYPE number.

    Args:
        dck_file (str): 解析対象の .dck ファイルパス / The path to the .dck file to analyze.
        type_no (int): 検索する TYPE 番号 / The TYPE number to search for.

    Returns:
        bool: TYPE 番号が見つかればTrue、見つからなければFalse / True if the TYPE number is found, else False.
    """
    pattern = re.compile(r"UNIT\s*(\d+)\s*TYPE\s*(\d+)")
    try:
        with open(dck_file, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
    except Exception as e:
        error_exit(f"Error reading file '{dck_file}': {e}")
    matches = pattern.findall(content)
    matches_type_no = [match for match in matches if match[1] == str(type_no)]
    return bool(matches_type_no)


def prompt_user_file_selection(matched_files):
    """
    候補ファイル一覧を表示し、ユーザに選択させたファイルの絶対パスを返す。
    Displays a list of candidate files to the user and returns the absolute path of the selected file.

    Args:
        matched_files (list): 選択可能なファイルのリスト / List of available candidate files.

    Returns:
        str: ユーザが選択したファイルの絶対パス / The absolute path of the file selected by the user.
    """
    print("\nThe Dck files containing the component are:")
    for index, file in enumerate(matched_files, start=1):
        print(f"{index} - {file}")
    print("")

    user_input = input("Enter the number of the file you want to open (q to quit): ")
    if user_input.lower() == "q":
        error_exit("Exiting...")
    if not user_input.isdigit():
        error_exit("A non-integer value was entered. Exiting...")

    no = int(user_input)
    if no < 1 or no > len(matched_files):
        error_exit("Invalid number. Exiting...")

    tpf_file = matched_files[no - 1]
    if not os.path.exists(tpf_file):
        error_exit(f"The file {tpf_file} does not exist. Exiting...")
    return os.path.abspath(tpf_file)


def find_tpf_files_by_type(type_no):
    """
    指定された TYPE 番号を含む .dck ファイルに関連する .tpf ファイルを検索し、
    ユーザに選択させた上で選択したファイルを開く。
    Searches for .tpf files associated with .dck files that contain the specified TYPE number,
    presents the available files to the user, and opens the selected file.

    Args:
        type_no (int): 検索する TYPE 番号 / The TYPE number to search for.
    """
    matched_tpf_files = []  # List of .tpf files
    for search_dir in directory_path:
        for dirpath, _, filenames in os.walk(search_dir):
            for filename in filenames:
                if filename.endswith(".dck"):
                    dck_file_path = os.path.join(dirpath, filename)
                    if contains_target_type(dck_file_path, type_no):
                        tpf_file_path = dck_file_path.replace(".dck", ".tpf")
                        matched_tpf_files.append(tpf_file_path)

    if not matched_tpf_files:
        error_exit("No file was found. Exiting...")

    available_tpf_files = []
    for target_tpf_file in matched_tpf_files:
        if not os.path.exists(target_tpf_file):
            dir_path = os.path.dirname(target_tpf_file)
            base_filename = os.path.splitext(os.path.basename(target_tpf_file))[0]
            for filename in os.listdir(dir_path):
                if filename.startswith(base_filename) and filename.endswith(".tpf"):
                    filename_path = os.path.join(dir_path, filename)
                    available_tpf_files.append(filename_path)
        else:
            available_tpf_files.append(target_tpf_file)

    if not available_tpf_files:
        error_exit("No available file was found. Exiting...")

    target_tpf_file = prompt_user_file_selection(available_tpf_files)
    print(f"Opening {target_tpf_file}...")
    subprocess.Popen(target_tpf_file, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "type_no",
        help="Specify the TYPE number to search. e.g. 56",
        type=int,
        nargs="?",  # Now optional when using -i/--initialize
    )
    parser.add_argument(
        "-p",
        "--path",
        help=r"""Specify the folder to search or export .dck files. 
e.g. C:\TRNSYS18\MyProjects\Project1
By default, the following folders are targeted.
   C:\TRNSYS18\Examples
   C:\TRNSYS18\Tess Models\Examples
   C:\TRNSYS18\TRNLib""",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--initialize",
        action="store_true",
        help="""Export .tpf files in the example folder to .dck format. 
If you are using findtype for the first time, be sure to export to .dck files using this option.""",
    )

    args = parser.parse_args()

    if args.initialize:
        # If -p is provided along with -i, use the -p folder for initialization.
        # Otherwise use the default directory_path.
        folders_to_export = [args.path] if args.path else directory_path
        print("Exporting .tpf files to .dck files...\n")
        for folder in folders_to_export:
            export_tpf_to_dck_files(folder)

    if args.type_no and not args.initialize:
        if args.path:
            # Override the default search directories with the folder specified by -p.
            directory_path = [args.path]
        find_tpf_files_by_type(args.type_no)
