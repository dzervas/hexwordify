"""
Console module
"""
import argparse
import sys
from hexwordify import finder


def main():
    """
    Main console function
    """
    parse = argparse.ArgumentParser(description=__doc__)
    parse.add_argument("-c", "--no-color", action="store_true",
                       help="Disable colored output")
    parse.add_argument("-p", "--prepend", action="store_true",
                       help="Prepend string given to output")
    parse.add_argument("-r", "--no-replace", action="store_true",
                       help="Ouput only found hex strings. Works like grep \
                            (only used if no hex arguments are given)")
    parse.add_argument("-s", "--min-size", type=int, default=32,
                       help="Minimum hex string size to search for in input \
                            (only used if no hex arguments are given)")
    parse.add_argument("strings", metavar="hex_string", nargs="*",
                       help="Hex strings to turn into words")
    parse.add_argument("-f", "--file", metavar="FILE", action="append",
                       help="File to read")
    args = parse.parse_args()

    if not args.strings and args.file is None:
        args.strings = sys.stdin.read().split("\n")
    elif args.strings:
        args.min_size = 0

    if args.file:
        args.strings = []
        for filep in args.file:
            with open(filep) as fileo:
                args.strings.append(fileo.read())

    result = finder(args.strings, min_size=args.min_size,
                    replace=not args.no_replace, prepend=args.prepend,
                    color=not args.no_color)

    if isinstance(result, list):
        print("\n".join(result).strip())
    else:
        print(result)


if __name__ == "__main__":
    main()
