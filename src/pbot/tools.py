import inspect

def func_as_tool(func):
    # Extract function name
    name = func.__name__

    # Extract function description
    doc = inspect.getdoc(func)
    description = doc.strip() if doc else ""

    # Extract function parameters
    signature = inspect.signature(func)
    parameters = {}
    required = []
    properties = {}

    for param_name, param in signature.parameters.items():
        # Get parameter annotation type
        annotation = param.annotation
        if annotation is inspect._empty:
            param_type = "string"  # default to string if no annotation
        else:
            if isinstance(annotation, str):
                # Forward reference, resolve the class
                cls = globals().get(annotation, str)
            else:
                cls = annotation
            if issubclass(cls, int):
                param_type = "integer"
            elif issubclass(cls, str):
                param_type = "string"
            elif issubclass(cls, bool):
                param_type = "boolean"
            else:
                param_type = "string"  # default to string for unknown types

        # Get parameter description from docstring
        param_desc = ""
        doc_lines = doc.splitlines() if doc else []
        for line in doc_lines:
            if line.strip().startswith(f"{param_name} "):
                desc_start = line.find(":") + 1
                param_desc = line[desc_start:].strip()
                break

        # Add to properties
        properties[param_name] = {
            "description": param_desc,
            "type": param_type
        }

        # Determine if parameter is required
        if param.default is inspect._empty:
            required.append(param_name)

    # Build parameters schema
    parameters_schema = {
        "type": "object",
        "properties": properties
    }
    if required:
        parameters_schema["required"] = required

    # Build the final tool dictionary
    tool_dict = {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters_schema
        }
    }

    return tool_dict

def register_tools(funcs):
    ret = []
    for func in funcs:
        ret.append(func_as_tool(func))
    return ret
