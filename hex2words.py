#!/usr/bin/env python3
"""
Turn hexadecimal strings to readable words.
By default uses bip-0039 bitcoin wordlist (2048 words).
If no hex arguments are given, script reads from stding and does
regex search for hex strings longer than `min_size` characters.

Example: gpg -k | hex2words.py
"""
import math
import os.path

WORDLIST_URL = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039"
WORDLIST_FILE = os.path.expanduser("~/.bip-0039.txt")


def transform(string):
    """
    Transforms a hexadecimal string to a string of words delimited with space
    """
    dictlist = []

    with open(WORDLIST_FILE, "r") as wordlist_file:
        wordlist_lines = wordlist_file.readlines()
        logarithm = int(math.log(len(wordlist_lines), 2))
        mask = 2**logarithm - 1

        # Split hex string to 64 bit integers (every character is 4 bits)
        for i in range(0, int(len(string) / 128) + bool(len(string) % 128)):
            hex_string = int(string[i * 128:(i + 1) * 128], 16)
            # Pad LS bits
            hex_string = hex_string << ((len(string) * 4) % logarithm)

            while hex_string > 0:
                hex_index = hex_string & mask
                dictlist.insert(0, wordlist_lines[hex_index].strip())
                hex_string = hex_string >> logarithm

    return dictlist


def wrapper(string, prepend, color):
    """Console wrapper. Takes care of coloring, append/prepend."""
    result = ""
    if prepend:
        result = string + ": "

    if color:
        result += "\x1b[32;1m"

    result += " ".join(transform(string))

    if color:
        result += "\x1b[0m"

    return result


def main():
    """Main console function"""
    import argparse
    import sys

    global WORDLIST_FILE

    parse = argparse.ArgumentParser(description=__doc__)
    parse.add_argument("-c", "--no-color", action="store_true",
                       help="Disable colored output")
    parse.add_argument("-l", "--lang", default="english", help="""
                       Language of dictionary to download/use \
                               (does not work with -w). Available languages:
                       chinese_simplified,
                       chinese_traditional,
                       english,
                       french,
                       italian,
                       japanese,
                       korean,
                       spanish
                       """)
    parse.add_argument("-p", "--prepend", action="store_true",
                       help="Prepend string given to output")
    parse.add_argument("-r", "--no-replace", action="store_true",
                       help="Ouput only found hex strings \
                            (only used if no hex arguments are given)")
    parse.add_argument("-s", "--min-size", type=int, default=32,
                       help="Minimum hex string size to search for in input \
                            (only used if no hex arguments are given)")
    parse.add_argument("-u", "--update", action="store_true",
                       help="Update (re-download) wordlist")
    parse.add_argument("-w", "--wordlist", default=WORDLIST_FILE,
                       help="Path to wordlist")
    parse.add_argument("strings", metavar="hex_string", nargs="*",
                       help="Hex strings to turn into words")
    args = parse.parse_args()

    WORDLIST_FILE = args.wordlist

    def wrapper_args(strings):
        """Simple wrapper to add arguments as needed"""
        return wrapper(strings[0], args.prepend, not args.no_color)

    if not os.path.exists(WORDLIST_FILE) or args.update:
        import urllib.request
        print("Downloading wordlist from %s" %
              (WORDLIST_URL + "/" + args.lang + ".txt"))
        urllib.request.urlretrieve(WORDLIST_URL + "/" + args.lang + ".txt",
                                   filename=WORDLIST_FILE)

        if args.update:
            exit()

    if args.strings:
        for string in args.strings:
            print(wrapper_args([string]))
    else:
        import re
        regex = re.compile(r"[0-9a-f]{%s}[0-9a-f]*" % args.min_size,
                           re.I | re.M)
        if args.no_replace:
            for string in re.findall(regex, sys.stdin.read()):
                print(wrapper_args([string]))
        else:
            print(re.sub(regex, wrapper_args, sys.stdin.read()).strip())


if __name__ == "__main__":
    main()
