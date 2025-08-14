from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

# operations = [get_files_info("calculator", "."),
#     get_files_info("calculator", "pkg"),
#     get_files_info("calculator", "/bin"),
#     get_files_info("calculator", "../")]

operations = [get_file_content("calculator", "main.py"),
    get_file_content("calculator", "pkg/calculator.py"),
    get_file_content("calculator", "pkg"),
    get_file_content("calculator", "/bin/cat"),
    get_file_content("calculator", "pkg/does_not_exist.py")]

for res in operations:
  print(res)
  print()
