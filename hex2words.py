#!/usr/bin/env python3
import math

wordlist_url = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/"

def hex2words(string, wordlist="wordlist.txt"):
    binstr = ""
    binlist = []
    dictlist = []

    # Hex to binary string
    for i in string:
        binstr += str(bin(int(i, 16))[2:].zfill(4))

    with open(wordlist, "r") as fp:
        fplist = fp.readlines()
        bitlen = int(math.log(len(fplist), 2))

        # Break binary string to log(len(wordlist_lines), 2) bit words
        for i in range(0, int(len(binstr) / bitlen) + bool(len(binstr) % bitlen)):
            binlist.append(int(binstr[i*bitlen:(i+1)*bitlen].zfill(bitlen), 2))

        for i in binlist:
            dictlist.append(fplist[i].strip())

    return dictlist

def hex2wordsWrap(hexa, wordlist, prepend, color):
    result = ""
    if prepend:
        result = hexa + ": "

    if color:
        result += "\x1b[32;1m"

    result += " ".join(hex2words(hexa, wordlist))

    if color:
        result += "\x1b[0m"

    return result

def main():
    import argparse
    import os.path
    import sys

    parse = argparse.ArgumentParser(description="""
            Turn hexadecimal strings to readable words.
            By default uses bip-0039 bitcoin wordlist (2048 words).
            If no hex arguments are given, script reads from stding and does
            regex search for hex strings longer than `min_size` characters.

            Example: gpg -k | hex2words.py
            """)
    parse.add_argument("-c", "--no-color", action="store_true", help="Disable colored output")
    parse.add_argument("-l", "--lang", default="english", help="""
                       Language of dictionary to download/use (does not work with -w). Available languages:
                       chinese_simplified,
                       chinese_traditional,
                       english,
                       french,
                       italian,
                       japanese,
                       korean,
                       spanish
                       """)
    parse.add_argument("-p", "--prepend", action="store_true", help="Prepend string given to output")
    parse.add_argument("-r", "--no-replace", action="store_true", help="Ouput only found hex strings (only used if no hex arguments are given)")
    parse.add_argument("-s", "--min-size", type=int, default=32, \
                       help="Minimum hex string size to search for in input (only used if no hex arguments are given)")
    parse.add_argument("-u", "--update", action="store_true", help="Update (re-download) wordlist")
    parse.add_argument("-w", "--wordlist", default=os.path.expanduser("~/.bip-0039.txt"), \
                       help="Path to wordlist")
    parse.add_argument("strings", metavar="hex_string", nargs="*", help="Hex strings to turn into words")
    args = parse.parse_args()

    if not os.path.exists(args.wordlist) or args.update:
        import urllib.request
        print("Downloading wordlist from %s" % (wordlist_url + args.lang + ".txt"))
        urllib.request.urlretrieve(wordlist_url + args.lang + ".txt", filename=args.wordlist)

        if args.update:
            exit()

    hex2wordsArgs = lambda x: hex2wordsWrap(x[0], args.wordlist, args.prepend, not args.no_color)

    if args.strings:
        for string in args.strings:
            print(hex2wordsArgs([string]))
    else:
        import re
        regex = re.compile(r"[0-9a-f]{%s}[0-9a-f]*" % args.min_size, re.I | re.M)
        if args.no_replace:
            for string in re.findall(regex, sys.stdin.read()):
                print(hex2wordsArgs([string]))
        else:
            print(re.sub(regex, hex2wordsArgs, sys.stdin.read()).strip())

if __name__ == "__main__":
    main()
