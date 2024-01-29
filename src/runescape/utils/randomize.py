import random
import string


def random_string(length: int = 10) -> str:
    """
    Generate a random string of a given length.

    Parameters
    ----------
    length : int, optional
        The length of the string.
        By default, 10.

    Returns
    -------
    str
        A random string.
    """
    return "".join(random.choices(string.ascii_letters, k=length))
