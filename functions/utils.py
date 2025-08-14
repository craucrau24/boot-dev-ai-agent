import pathlib

def check_path_is_in_working_directory(pwd, path_to_check):
  return str(path_to_check).startswith(str(pathlib.Path(pwd).resolve()))