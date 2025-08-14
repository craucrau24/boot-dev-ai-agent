import pathlib

from .utils import check_path_is_in_working_directory

def write_file(working_directory, file_path, content):
  abs_path = pathlib.Path(working_directory, file_path).resolve()

  if not check_path_is_in_working_directory(working_directory, abs_path):
    return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

  try:
    abs_path.write_text(content)
  except IOError as exc:
    return f"Error: Cannot write {file_path} - {exc}"

  return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    