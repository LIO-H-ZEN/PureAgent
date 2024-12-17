import pdb
from agents import ThreadSafeList

def pretty_print_nested(obj, indent=0, omit_limit=100):
    half = int(omit_limit / 2)
    indent_str = ' ' * indent
    if isinstance(obj, str):
        if len(obj) > omit_limit:
            return obj[:half] + '...' + obj[-half:]
        else:
            return obj
    elif isinstance(obj, list) or isinstance(obj, ThreadSafeList):
        if not obj:
            return '[]'
        elements = [pretty_print_nested(elem, indent + 4) for elem in obj]
        elements_str = ',\n'.join([f'{indent_str}    {elem}' for elem in elements])
        return f'[\n{elements_str}\n{indent_str}]'
    elif isinstance(obj, dict):
        if not obj:
            return '{}'
        pairs = []
        for k, v in obj.items():
            key_str = pretty_print_nested(k)
            val_str = pretty_print_nested(v, indent + 4)
            pairs.append(f"{key_str}: {val_str}")
        pairs_str = ',\n'.join([f'{indent_str}    {pair}' for pair in pairs])
        return f'{{\n{pairs_str}\n{indent_str}}}'
    else:
        return str(obj)
