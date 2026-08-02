from is_prime_module import is_prime
import pytest


@pytest.mark.parametrize("n", [-100, -10, -2, -1])
def test_negative_numbers(n):
    """Negatif sayıların asal olmadığını (False) doğrular."""
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [0, 1])
def test_boundary_zero_and_one(n):
    """Sınır değerleri olan 0 ve 1'in asal olmadığını (False) doğrular."""
    assert is_prime(n) is False


def test_smallest_prime():
    """En küçük asal sayı olan 2'yi doğrular."""
    assert is_prime(2) is True


@pytest.mark.parametrize("n", [3, 5, 7, 11, 13, 17, 19, 23, 29, 31])
def test_small_primes(n):
    """Küçük asal sayıların True döndürdüğünü doğrular."""
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 27])
def test_small_composite_numbers(n):
    """Küçük bileşik (asal olmayan) sayıların False döndürdüğünü doğrular."""
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [4, 9, 16, 25, 36, 49, 64, 81, 100, 121])
def test_perfect_squares(n):
    """Tam kare sayıların (kök sınırı kontrolü dahil) False döndürdüğünü doğrular."""
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [7919, 9973, 104729, 15485863])
def test_large_primes(n):
    """Büyük asal sayıların True döndürdüğünü doğrular."""
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [8000, 9999, 104730, 1000000, 15485864])
def test_large_composite_numbers(n):
    """Büyük asal olmayan (bileşik) sayıların False döndürdüğünü doğrular."""
    assert is_prime(n) is False
