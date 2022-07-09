import pytest

from functools import reduce
from libnum.factorize import factorize
from libnum.factorize import is_power


def test_powers():
    numbers = [2, 3, 5, 6, 7, 10, 1993, 1995]
    pows = [2, 3, 4, 5, 6, 7, 8, 10, 30]
    for n in numbers:
        for k in pows:
            val = n ** k
            assert is_power(val) == (n, k)


def test_not_powers():
    numbers = [2, 3, 5, 6, 7, 10, 1993, 1995]
    for n in numbers:
        assert not is_power(n)


def test_samples():
    test_lists = [
        set([(3, 1), (5, 5), (19, 2), (1993, 1), (37, 1), (2, 4)]),
        set([(2, 100), (3, 50), (5, 20), (7, 15), (11, 10), (13, 5)]),
        set([(1993, 5)]),
        set([(2, 4000)]),
    ]

    for primes_list in test_lists:
        while primes_list:
            n = reduce(lambda a, b: a * (b[0] ** b[1]), primes_list, 1)
            primes_list_test = set(sorted(factorize(n).items()))
            assert primes_list == primes_list_test
            primes_list.pop()


def test_zero():
    assert factorize(0) == {0: 1}


def test_small():
    assert factorize(1) == {1: 1}
    assert factorize(2) == {2: 1}
    assert factorize(3) == {3: 1}
    assert factorize(4) == {2: 2}
    assert factorize(5) == {5: 1}
    assert factorize(6) == {2: 1, 3: 1}
    assert factorize(7) == {7: 1}
    assert factorize(8) == {2: 3}
    assert factorize(9) == {3: 2}
    assert factorize(10) == {2: 1, 5: 1}


def test_small_negative():
    assert factorize(-1) == {-1: 1}
    assert factorize(-2) == {-1: 1, 2: 1}
    assert factorize(-3) == {-1: 1, 3: 1}
    assert factorize(-4) == {-1: 1, 2: 2}
    assert factorize(-5) == {-1: 1, 5: 1}
    assert factorize(-6) == {-1: 1, 2: 1, 3: 1}
    assert factorize(-7) == {-1: 1, 7: 1}
    assert factorize(-8) == {-1: 1, 2: 3}
    assert factorize(-9) == {-1: 1, 3: 2}
    assert factorize(-10) == {-1: 1, 2: 1, 5: 1}


def test_errors():
    with pytest.raises(TypeError):
        factorize("1")
    with pytest.raises(TypeError):
        factorize(10.3)
    with pytest.raises(TypeError):
        factorize(complex(10, 3))
    with pytest.raises(TypeError):
        factorize((2, 3))
