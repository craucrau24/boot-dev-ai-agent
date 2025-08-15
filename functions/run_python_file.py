import pathlib
import subprocess

from google.genai import types

from .utils import check_path_is_in_working_directory

def run_python_file(working_directory, file_path, args=[]):
  abs_path = pathlib.Path(working_directory, file_path).resolve()

  if not check_path_is_in_working_directory(working_directory, abs_path):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  if not abs_path.exists():
    return f'Error: File "{file_path}" not found.'

  if not str(abs_path).endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'

  try:
    cmd = subprocess.run(["python", abs_path, *args], capture_output=True, cwd=working_directory, timeout=30)
    if len(cmd.stdout) != 0 or len(cmd.stderr) != 0:
      output = f"STDOUT: \n{cmd.stdout.decode(errors="replace")}\nSTDERR: \n{cmd.stderr.decode(errors="replace")}\n"
    else:
      output = "No output produced\n"
    status = f"Process exited with code {cmd.returncode}\n" if cmd.returncode != 0 else ""
    return output + status
  except Exception as e:
    return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Run a python file, constrained to the working directory.",
  parameters=types.Schema(
      type=types.Type.OBJECT,
      properties={
          "file_path": types.Schema(
              type=types.Type.STRING,
              description="The path of the file to run, relative to the working directory",
          ),
      },
  ),
)