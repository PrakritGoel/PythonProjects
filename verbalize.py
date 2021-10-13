"""
The program uses recursion to convert a number to its spoken value. Some
examples here explain it better
$ python3 verbalize.py 123456789
one hundred twenty-three million
four hundred fifty-six thousand
seven hundred eighty-nine

This is achieved by reading the information from a file, that contains the
verbal representation of all numbers from 0-20, followed by all multiples
of 10, up to 90, and then, by powers of 10, up to a centillion. The program
then uses recursion to break down a number, and use the above information
for the representation as illustrated above.

Per the guide lines given in the assignment, the program uses only a single
loop; to read the contents of the given file. The rest of the logic is
implemented using recursion and iterators.
"""
import sys


def str_for_nums_less_than_thousand(value: int, short_list_iter, verbal_dict) -> str:
    """
    Numbers one to thousand are returned as a single string, with the components of numbers
    less than a hundred separated by a '-'. This function does that magic.
    param value: Input integer value less than 1000
    param short_list_iter: Iterator object for strings for numbers less than 1000
    return: string representation of the number based on rules in verbalize
    """
    return_str = ''

    if value == 0:
        return 'zero'

    next_key = next(short_list_iter)

    # Need to explicitly check for the key being 100, since otherwise, for the input 100
    # the string 'hundred' will be returned instead of 'one hundred'
    if value % next_key == 0 and next_key != 100:
        return_str += verbal_dict[next_key]
        return return_str

    quotient = value // next_key
    remainder = value % next_key

    if quotient > 0:
        if next_key == 100:
            return_str += verbal_dict[quotient] + ' '
        return_str += verbal_dict[next_key]

        if remainder == 0:
            return return_str

        # if remainder < 10:
        if 20 <= next_key < 100:
            return_str += '-'
        else:
            return_str += ' '

    return_str += str_for_nums_less_than_thousand(remainder, short_list_iter, verbal_dict)
    return return_str


def quotient_and_remainder(value: int, keys_iterator, verbal_dict):
    """
    Evaluate and return the quotient, remainder, and the next key. The
    function makes repeated recursive calls, dividing the value with
    the next element returned by the iterator, till the quotient is
    non-zero. The key that gives a non-zero quotient is returned
    along with the quotient and remainder.
    param value: Number that needs to be broken down in quotient/remainder
    param keys_iterator: The iterator that stores the keys.
    param verbal_dict: The keys dictionary
    return:
    """
    next_key = next(keys_iterator)

    quotient = value // next_key
    remainder = value % next_key

    if quotient == 0:
        return quotient_and_remainder(value, keys_iterator, verbal_dict)

    return quotient, remainder, next_key


def verbalize(value: int) -> list[str]:
    """
    Returns a list of the verbalized orders of magnitude of a natural number, e.g.:
    verbalize(0) --> ['zero']
    verbalize(42) --> ['forty-two']
    verbalize(101) --> ['one hundred one']
    verbalize(9999) --> ['nine thousand', 'nine hundred ninety-nine']
    verbalize(1234567) -->
    ['one million', 'two hundred thirty-four thousand', 'five hundred sixty-seven']
    """
    with open('/srv/datasets/number_names.txt', 'r') as file_handle:
        data = file_handle.readlines()

    verbal_dict = dict()
    for line in data:
        line = line.strip()
        val, key = line.split(' ')
        verbal_dict[int(key)] = val

    # Create an iterator for the keys in the dictionary
    keys_iterator = reversed(verbal_dict.keys())

    # Create an iterator object for keys less than 1000
    short_list_iter = reversed(list(verbal_dict.keys())[:29])

    if value < 1000:
        return [(str_for_nums_less_than_thousand(value, short_list_iter, verbal_dict))]

    quotient, remainder, next_key = quotient_and_remainder(value, keys_iterator, verbal_dict)

    if quotient > 0:
        return_list = [str_for_nums_less_than_thousand(quotient, short_list_iter, verbal_dict) + ' '
                       + verbal_dict[next_key]]
        if remainder == 0:
            return return_list

        remainder_list = verbalize(remainder)
        return_list.extend(remainder_list)
        return return_list

    return verbalize(remainder)


if __name__ == '__main__':
    print('\n'.join(verbalize(int(sys.argv[1]))))
