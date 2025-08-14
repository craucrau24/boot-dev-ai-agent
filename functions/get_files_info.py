import pathlib

from .utils import check_path_is_in_working_directory

def get_files_info(working_directory, directory="."):
  try:
    abs_path = pathlib.Path(working_directory, directory).resolve()
  except:
    return f"Error: couldn't resolve {directory}"

  if not check_path_is_in_working_directory(working_directory, abs_path):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

  if not abs_path.is_dir():
    return f'Error: "{directory}" is not a directory'

  dir_name = f"'{directory}'" if directory != "." else "current"
  header = f"Result for {dir_name} directory:\n"
  return header + "\n".join((f" - {chld.name}: file_size={stats.st_size} bytes, is_dir={chld.is_dir()}" for chld, stats in map(lambda child: (child, child.stat()), abs_path.iterdir())))