from __future__ import unicode_literals

import random
from random import randint


# Don't use l or 1 because sometimes hard to tell them apart. Don't use o, O or
# 0 since hard to tell those apart too.
NUMBERS = ('2', '3', '4', '5', '6', '7', '8', '9')
LETTERS_LOWER = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm',
                 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
LETTERS_UPPER = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                 'Z')
LETTERS = LETTERS_LOWER + LETTERS_UPPER
ALPHANUM = NUMBERS + LETTERS
ALPHANUM_LOWER = NUMBERS + LETTERS_LOWER


def random_alphanum(length=10, lower_only=False):
    """
    Gets a random alphanumeric value using both letters and numbers.

    :param length: size of the random alphanumeric string.
    :param lower_only: boolean indicating if only lower case letters should be
        used.
    :return: alphanumeric string size of length

    This function uses all number except for:

    * 0
    * 1

    and uses all letters except for:

    * lower case "l" (el)
    * lower and upper case "o" and "O" (oh)

    For upper and lower cased letters...
    ------------------------------------
    Upper and lower cased letters and numbers can be used more than once which
    leaves the possible combinations as follows:

        8 numbers used + 49 letters used (upper and lower) = 57 total characters

    Which leads us to the following equation:

        57 total characters ^ length = total possible combinations

    The following total possible combinations are below for a given length:

        57 ^ 1 = 57
        57 ^ 2 = 3,249
        57 ^ 3 = 185,193
        57 ^ 4 = 10,556,001
        57 ^ 5 = 601,692,057
        57 ^ 6 = 34,296,447,249
        57 ^ 7 = 1,954,897,493,193
        57 ^ 8 = 111,429,157,112,001
        57 ^ 9 = 6,351,461,955,384,057
        57 ^ 10 = 362,033,331,456,891,249
        ...

    For lower cased letters...
    --------------------------
    Lower cased letters and numbers can be used more than once which leaves the
    possible combinations as follows:

        8 numbers used + 24 letters used (lower only) = 32 total characters

    Which leads us to the following equation:

        32 total characters ^ length = total possible combinations

    The following total possible combinations are below for a given length:

        32 ^ 1 = 32
        32 ^ 2 = 1,024
        32 ^ 3 = 32,768
        32 ^ 4 = 1,048,576
        32 ^ 5 = 33,554,432
        32 ^ 6 = 1,073,741,824
        32 ^ 7 = 34,359,738,368
        32 ^ 8 = 1,099,511,627,776
        32 ^ 9 = 35,184,372,088,832
        32 ^ 10 = 1,125,899,906,842,624
        ...

    """
    character_set = ALPHANUM_LOWER if lower_only else ALPHANUM
    chars = random.sample(character_set, 25)

    while len(chars) < length:
        chars += random.sample(character_set, 25)

    random.shuffle(chars)
    return ''.join(chars[:length])


def generate_key(low=7, high=10, lower_only=False):
    """Gets a random alphanumeric key between low and high characters in
    length.
    """
    return random_alphanum(length=randint(7, 10), lower_only=lower_only)
