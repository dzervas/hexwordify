# Hex2Words

This is a simple script that finds hex strings to the input given and maps it
to words with the [`bip-0039`](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) wordlist.
The main idea for the creation of this script is to make GPG fingerprint check
easier.

## Usage
```
usage: hex2words.py [-h] [-c] [-p] [-r] [-s MIN_SIZE]
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
  -p, --prepend         Prepend string given to output
  -r, --no-replace      Ouput only found hex strings (only used if no hex
                        arguments are given)
  -s MIN_SIZE, --min-size MIN_SIZE
                        Minimum hex string size to search for in input (only
                        used if no hex arguments are given)
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

dzervas ~> gpg --list-public-keys dzervas@dzervas.gr | hex2words
pub   rsa4096 2015-01-25 [SC]
      coral evolve fitness stuff rebuild able fringe loud dice tumble pact snap express cycle object
uid           [ultimate] Dimitris Zervas <dzervas@dzervas.gr>
uid           [ultimate] Dimitris Zervas <01ttouch@gmail.com>
uid           [ultimate] Dimitris Zervas <dzervas@tolabaki.gr>
uid           [ultimate] Dimitris Zervas <csd3502@csd.uoc.gr>
uid           [ultimate] Dimitris Zervas <dzervas@ics.forth.gr>
sub   rsa4096 2015-01-25 [E]
```
