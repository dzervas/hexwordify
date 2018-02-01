"""
Console module
"""
from hexwordify import wrapper


def main():
    """
    Main console function
    """
    import argparse
    import sys

    parse = argparse.ArgumentParser(description=__doc__)
    parse.add_argument("-c", "--no-color", action="store_true",
                       help="Disable colored output")
    parse.add_argument("-p", "--prepend", action="store_true",
                       help="Prepend string given to output")
    parse.add_argument("-r", "--no-replace", action="store_true",
                       help="Ouput only found hex strings \
                            (only used if no hex arguments are given)")
    parse.add_argument("-s", "--min-size", type=int, default=32,
                       help="Minimum hex string size to search for in input \
                            (only used if no hex arguments are given)")
    parse.add_argument("strings", metavar="hex_string", nargs="*",
                       help="Hex strings to turn into words")
    args = parse.parse_args()

    def wrapper_args(strings):
        """Simple wrapper to add arguments as needed"""
        # try:
            # return wrapper(strings[0], args.prepend, not args.no_color)
        # except TypeError:
        return wrapper(strings.group(0), args.prepend, not args.no_color)

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
