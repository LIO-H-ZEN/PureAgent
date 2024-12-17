import sympy

from tools import register_tools
from utils import pretty_print_nested

def is_lucky(x: int) -> bool:
    """Determine whether the input number is a lucky number.

    Args:
        x (int): The input number to be checked.

    Returns:
        bool: True if the number is a lucky number, False otherwise.
    """
    return sympy.isprime(x + 3)

print(pretty_print_nested(register_tools([is_lucky])))
