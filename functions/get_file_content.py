import pathlib

from .utils import check_path_is_in_working_directory

def get_file_content(working_directory, file_path):
  try:
    abs_path = pathlib.Path(working_directory, file_path).resolve()
  except:
    return f"Error: couldn't resolve {file_path}"

  if not check_path_is_in_working_directory(working_directory, abs_path):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

  if not abs_path.is_file():
    return f'Error: File not found or is not a regular file: "{file_path}"'

  with open(abs_path, "r") as f:
    try:
      contents = f.read(10000)
      if len(f.read(1)) != 0:
        contents += f"[...File \"{file_path}\" truncated at 10000 characters]"
    except IOError as e:
        return f"Error: error reading file \"{file_path}\" - {e}"

  return contents