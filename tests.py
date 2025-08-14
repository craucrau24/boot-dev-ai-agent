from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# operations = [get_files_info("calculator", "."),
#     get_files_info("calculator", "pkg"),
#     get_files_info("calculator", "/bin"),
#     get_files_info("calculator", "../")]

# operations = [get_file_content("calculator", "main.py"),
#     get_file_content("calculator", "pkg/calculator.py"),
#     get_file_content("calculator", "pkg"),
#     get_file_content("calculator", "/bin/cat"),
#     get_file_content("calculator", "pkg/does_not_exist.py")]

operations = [write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
write_file("calculator", "/tmp/temp.txt", "this should not be allowed")]

for res in operations:
  print(res)
  print()
