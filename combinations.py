'''
This program receives two positive integers (n and k) as inputs, and generates
all possible combinations of size k, given a larger number n. For example, if
the program is invoked as
$ python3 combinations.py 4 2
{1, 2}
{1, 3}
{1, 4}
{2, 3}
{2, 4}
{3, 4}
'''

import sys

MAX_SIZE = 100


def print_set(n):
    """
    This function prints a particular set of size k.
    All elements in array B, that have the bit field set to 1
    are printed. Others are ignored
    """
    add_comma_flag = 0

    sys.stdout.write("{")
    for i in range(1, n+1):
        if B[i] == 1:
            if add_comma_flag == 0:
                sys.stdout.write("{}".format(i))
                add_comma_flag = 1
            else:
                sys.stdout.write(", {}".format(i))
    print("}")


def print_subsets(n, k, i):
    """
    This function generates the combinations for given values of n and k.
    It uses the provided recursive algorithm.
    """
    if k > n - i + 1:
        return

    if k == 0:
        print_set(n)
        return

    B[i] = 1
    print_subsets(n, k-1, i+1)
    B[i] = 0
    print_subsets(n, k, i+1)


def print_error_msg():
    """
    Print the usage error message.
    """
    print("Usage: " + sys.argv[0] + " n k (n and k are ints satisfying 0<=k<=n<=100)")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_error_msg()
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
    except ValueError:
        print_error_msg()
        sys.exit(1)

    if k > n or n > MAX_SIZE:
        print_error_msg()
        sys.exit(1)

    B = [0 for i in range(MAX_SIZE+1)]
    print_subsets(n, k, 1)
