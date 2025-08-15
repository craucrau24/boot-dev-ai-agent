from google.genai import types

from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file

functions = {
  "get_files_info": get_files_info,
  "get_file_content": get_file_content,
  "run_python_file": run_python_file,
  "write_file": write_file,
}

def call_function(function_call_part: types.FunctionCall, verbose=False):
  if verbose:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f"Calling function: {function_call_part.name}")

  function_name = function_call_part.name
  if function_name is None: function_name = ""

  func = functions.get(function_name)
  args = function_call_part.args
  if args is None: args = {}

  if callable(func):
    function_result = func("./calculator", **args)
    return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_name,
              response={"result": function_result},
          )
      ],
  )
  else:
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
