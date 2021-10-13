"""
This program creates two generators
* a prime number generator
* a semi-prime number generator
  (Semi prime numbers are the product of two prime numbers).
Additionally, it provides several functions that use these iterators to
generate information that might be of interest, e.g.
1. A possibly infinite sequence of prime/sub-primes numbers.
2. All prime/sub-prime numbers below a given threshold.
3. The nth prime/sub-prime number.
4. Prime factors of a given number
"""

from collections.abc import Callable, Iterator

from typing import List
import math


def elements_under(sequence: Iterator[int], bound: int, predicate: Callable[[int], bool] = None) \
        -> Iterator[int]:
    """
    Yields a finite sequence of elements under a given bound, optionally matching a predicate.

    :param sequence: an infinite sequence of integers, e.g. primes()
    :param bound:  an exclusive upper bound for the yielded sequence
    :param predicate: if present, the sequence includes only values for which this function
     returns True
    """
    item = next(sequence)

    while item < bound:
        if predicate is not None:
            if predicate(item):
                yield item
        else:
            yield item
        item = next(sequence)


def is_prime(n: int) -> bool:
    """ Returns whether n is prime. """
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def nth_element(sequence: Iterator[int], n: int) -> int:
    """
    Returns the nth element of a possibly infinite sequence of integers.

    :param sequence: a sequence of integers, e.g. primes()
    :param n: the sequence index desired
    :return: the value at index n of the sequence
    """
    for _ in range(n):
        next(sequence)

    return next(sequence)


def primes() -> Iterator[int]:
    """ Yields an infinite sequence of prime numbers. """
    yield 2
    n = 3

    while True:
        if is_prime(n):
            yield n
        n += 2


def prime_factors(n: int) -> List[int]:
    """ Returns a list of prime numbers with product n, in ascending order. """
    p_gen = primes()
    p_num = next(p_gen)
    factors = []

    while n != 1:
        if n % p_num == 0:
            factors.append(p_num)
            n /= p_num
        else:
            p_num = next(p_gen)

    return factors


def semiprimes() -> Iterator[int]:
    """ Yields an infinite sequence of semiprimes. """
    val = 1

    while True:
        if len(prime_factors(val)) == 2:
            yield val
        val += 1


if __name__ == '__main__':
    assert all(is_prime(n) for n in (2, 3, 5, 7))
    assert all(not is_prime(n) for n in (4, 6, 8, 9))
    assert list(elements_under(primes(), 10)) == [2, 3, 5, 7]
    assert list(elements_under(semiprimes(), 10)) == [4, 6, 9]
    assert nth_element(primes(), 2) == 5
    assert nth_element(semiprimes(), 2) == 9
    assert list(elements_under(primes(), 1386, lambda p: not 1386 % p)) == [2, 3, 7, 11]
    assert prime_factors(1386) == [2, 3, 3, 7, 11]
