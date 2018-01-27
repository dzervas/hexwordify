# Hex2Words

This is a simple script that finds hex strings to the input given and maps it
to words with the [`bip-0039`](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) wordlist.
The main idea for the creation of this script is to make GPG fingerprint check
easier.

## Usage
```
hex2words.py [-h] [-c] [-l LANG] [-p] [-r] [-s MIN_SIZE] [-u]
                    [-w WORDLIST]
                    [hex_string [hex_string ...]]

Turn hexadecimal strings to readable words. By default uses bip-0039 bitcoin
wordlist (2048 words). If no hex arguments are given, script reads from stding
and does regex search for hex strings longer than `min_size` characters.
Example: gpg -k | hex2words.py

positional arguments:
  hex_string            Hex strings to turn into words

optional arguments:
  -h, --help            show this help message and exit
  -c, --no-color        Disable colored output
  -l LANG, --lang LANG  Language of dictionary to download/use (does not work
                        with -w). Available languages: chinese_simplified,
                        chinese_traditional, english, french, italian,
                        japanese, korean, spanish
  -p, --prepend         Prepend string given to output
  -r, --no-replace      Ouput only found hex strings (only used if no hex
                        arguments are given)
  -s MIN_SIZE, --min-size MIN_SIZE
                        Minimum hex string size to search for in input (only
                        used if no hex arguments are given)
  -u, --update          Update (re-download) wordlist
  -w WORDLIST, --wordlist WORDLIST
                        Path to wordlist
```

## Example
```
dzervas ~> gpg --list-public-keys dzervas@dzervas.gr
pub   rsa4096 2015-01-25 [SC]
      1814E2AFF5E59A004BA2109EBEA53D73528636D3
uid           [ultimate] Dimitris Zervas <dzervas@dzervas.gr>
uid           [ultimate] Dimitris Zervas <01ttouch@gmail.com>
uid           [ultimate] Dimitris Zervas <dzervas@tolabaki.gr>
uid           [ultimate] Dimitris Zervas <csd3502@csd.uoc.gr>
uid           [ultimate] Dimitris Zervas <dzervas@ics.forth.gr>
sub   rsa4096 2015-01-25 [E]

dzervas ~> gpg --list-public-keys dzervas@dzervas.gr | ~/Lab/hex2words/hex2words.py
pub   rsa4096 2015-01-25 [SC]
      blossom poem program type fluid ability company dragon pact vivid exercise trade chronic bread act
uid           [ultimate] Dimitris Zervas <dzervas@dzervas.gr>
uid           [ultimate] Dimitris Zervas <01ttouch@gmail.com>
uid           [ultimate] Dimitris Zervas <dzervas@tolabaki.gr>
uid           [ultimate] Dimitris Zervas <csd3502@csd.uoc.gr>
uid           [ultimate] Dimitris Zervas <dzervas@ics.forth.gr>
sub   rsa4096 2015-01-25 [E]
```
