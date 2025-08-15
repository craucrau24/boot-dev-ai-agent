import pathlib

from google.genai import types

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
    
schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Write data to a file, constrained to the working directory. If file exists, its content will be overwritten. Otherwise a new file will be created",
  parameters=types.Schema(
      type=types.Type.OBJECT,
      properties={
          "file_path": types.Schema(
              type=types.Type.STRING,
              description="The path of the file to execute, relative to the working directory.",
          ),
          "content": types.Schema(
              type=types.Type.STRING,
              description="The data to be written in the file",
          ),
      },
  ),
)