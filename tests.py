from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def run_tests():
    
    # print(run_python_file("calculator", "main.py"))
    # print()
    # print(run_python_file("calculator", "main.py", ["3 + 5"]))
    # print()
    # print(run_python_file("calculator", "tests.py"))
    # print()
    # print(run_python_file("calculator", "../main.py"))
    # print()
    # print(run_python_file("calculator", "nonexistent.py"))
    print(get_file_content(working_directory='calculator', file_path='main.py'))

if __name__ == "__main__":
    run_tests()
