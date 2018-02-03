"""
Turn hexadecimal strings to readable words.
By default uses bip-0039 bitcoin wordlist (2048 words).
If no hex arguments are given, script reads from stding and does
regex search for hex strings longer than `min_size` characters.

Example: gpg -k | hexwordify.py
"""
import math
import re
try:
    from .bip_0039 import WORDLIST
except (ImportError, ValueError):
    from bip_0039 import WORDLIST


# The list is not altered, so its not a dangerous default value anymore:
# pylint: disable=dangerous-default-value
def transform(string, wordlist=WORDLIST):
    """
    Transforms a hexadecimal string to a string of words delimited with space.

    string: <str> Hex string to transform
    wordlist: <tuple, list> Tuple containing words (duh...)
              Length is recommended to be a power of 2

    return value: <list> List containing resulting words

    Example:
        >>> hexwordify.transform("DEADBEEF")
            ['dash', 'fork', 'upon', 'length']
    """
    dictlist = []

    if not isinstance(string, str):
        raise TypeError("String has to be str (wtf man?)")

    if not isinstance(wordlist, (list, tuple)):
        raise TypeError("Wordlist has to be tuple or list")

    if len(wordlist) < 1:
        return []

    string = string.replace(":", "")
    logarithm = int(math.log(len(wordlist), 2))
    mask = 2**logarithm - 1

    # Split hex string to 64 bit integers (every character is 4 bits)
    for i in range(0, int(len(string) / 128) + bool(len(string) % 128)):
        # Parse string as hex
        hex_string = int(string[i * 128:(i + 1) * 128], 16)
        # Pad LS bits
        hex_string = hex_string << ((len(string) * 4) % logarithm)

        while hex_string > 0:
            hex_index = hex_string & mask
            dictlist.insert(0, wordlist[hex_index].strip())
            hex_string = hex_string >> logarithm

    return dictlist


def wrapper(string, prepend=True, color=False):
    """
    Console wrapper. Takes care of coloring and original string appending

    string: <str> Hex string to transform
    prepend: <bool> Prepend given string to result
    color: <bool> Add bash color escape codes

    return value: <str> Returns the result as a space delimited string

    Example:
        >>> hexwordify.wrapper("DEADBEEF", False, False)
            'dash fork upon length'
    """
    result = ""
    if prepend:
        result = string + ": "

    if color:
        result += "\x1b[32;1m"

    result += " ".join(transform(string))

    if color:
        result += "\x1b[0m"

    return result.strip()


def finder(vals, min_size=16, replace=True, prepend=False, color=False):
    """
    Function that finds hexadecimal values and transforms them.

    vals: <str, int, float, list, tuple, dict> Values to be searched
            The string can include semicolons (:)
    prepend: <bool> Prepend the found string to the resulting words
    color: <bool> Add terminal color escape codes
    min_size: <int> Minimum consecutive characters that have to be found to be
                    considered a hex string
    replace: <bool> Replace the found string with the resulting words

    return value:
        if vals is <str, int, float> a <str> of space delimited words
        if vals is <list, tuple> a <list> with the appropriate return value for
            each item (see examples)
        if vals is <dict> a <dict> with the appropriate return value for each
            item (see examples)

    Examples:
        >>> hexwordify.finder("DEADBEEFDEADBEEF")
            'assume fine wing wink pumpkin wash scale'
        >>> hexwordify.finder(0xDEADBEEFDEADBEEF)
            'assume fine wing wink pumpkin wash scale'
        >>> hexwordify.finder(["DEADBEEFDEADBEEF", 0x1234567890ABCDEF])
            ['assume fine wing wink pumpkin wash scale',
            'ability cash clinic time betray social job']
        >>> hexwordify.finder({"a": "DEADBEEFDEADBEEF", \
                "b": 0x1234567890ABCDEF})
            {'a': 'assume fine wing wink pumpkin wash scale',
            'b': 'ability cash clinic time betray social job'}
        >>> hexwordify.finder({"a": "this is a test DEADBEEFDEADBEEF", \
                "b": 0x1234567890ABCDEF}, replace=False)
            {'a': 'this is a test assume fine wing wink pumpkin wash scale',
            'b': 'ability cash clinic time betray social job'}
    """
    def wrapper_args(matches):
        """Simple wrapper to add arguments as needed"""
        return wrapper(matches.group(0), prepend, color)

    if isinstance(vals, float):
        return finder(int(vals), min_size, replace, prepend, color)

    if isinstance(vals, int):
        return finder(hex(vals), min_size, replace, prepend, color)

    if isinstance(vals, (list, tuple)):
        result = []

        for val in vals:
            result.append(finder(val, min_size, replace, prepend, color))

        return result

    if isinstance(vals, dict):
        result = {}

        for key in vals:
            result[key] = finder(vals[key], min_size, replace, prepend, color)

        return result

    if isinstance(vals, str):
        regex = re.compile(r"(?:0x)?[0-9a-f:]{%s,}" % min_size, re.I | re.M)

        if replace:
            return re.sub(regex, wrapper_args, vals).strip()

        for val in re.findall(regex, vals):
            return wrapper(val, prepend, color)

    raise TypeError("'vals' can be str, int, float, list, tuple, dict")
