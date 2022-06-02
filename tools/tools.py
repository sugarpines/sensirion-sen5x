def create_dir(path: str) -> None:
    """
    Creates directory in path if it doesn't exist
    :param path: path to directory
    """
    from os import mkdir
    try:
        mkdir(path)
    except OSError as e:
        if e.errno == 17:  # already exists
            pass
        else:
            raise


def round_to_int(value: float, round_to: int = 1) -> [int]:
    """
    Rounds float value to nearest <round_to> integer
    For example:
        value = 12.4 and round_to = 5 will return 10
        value = 12.6 and round_to = 5 will return 15
    :param value: value to round
    :param round_to: integer to round to
    :type round_to:
    :return: rounded value
    """
    return int(round_to * round(value / round_to))


def round_to_half(value: float) -> [float]:
    """ Rounds value to nearest 0.5 or ignores if None """
    return round(value * 2) / 2


def all_ones(b: bytes) -> bool:
    """
    Returns True if all bits are 1
    :param b: bytes
    :return: True if all 1's else False
    """
    n = int.from_bytes(b, 'big')
    return ((n + 1) & n == 0) and (n != 0)


def c_to_f(c: float) -> float:
    """
    Converts °Celsius to °Fahrenheit
    """
    return (c * 9 / 5) + 32
