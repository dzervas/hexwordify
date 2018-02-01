"""
Turn hexadecimal strings to readable words.
By default uses bip-0039 bitcoin wordlist (2048 words).
If no hex arguments are given, script reads from stding and does
regex search for hex strings longer than `min_size` characters.

Example: gpg -k | hexwordify.py
"""
import math
try:
    from .bip_0039 import WORDLIST
except (ImportError, ValueError):
    from bip_0039 import WORDLIST


# The list is not altered, so its not a dangerous default value anymore:
# pylint: disable=dangerous-default-value
def transform(string, wordlist=WORDLIST):
    """
    Transforms a hexadecimal string to a string of words delimited with space.
    """
    dictlist = []

    if len(wordlist) < 1:
        return []

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


def wrapper(string, prepend, color):
    """
    Console wrapper. Takes care of coloring and original string appending
    """
    result = ""
    if prepend:
        result = string + ": "

    if color:
        result += "\x1b[32;1m"

    result += " ".join(transform(string))

    if color:
        result += "\x1b[0m"

    return result
