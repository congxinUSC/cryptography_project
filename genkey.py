"""This script generate RSA public and private keys."""
import sys
import random
import math

DEFAULT_KEY_LENGTH = 1024
FALSE_PRIME_TOLERANCE_POWER = -128
PUBLIC_KEY = 65537


class GenKey(object):
    """RSA key pair generator. Using sys.SystemRandom() to generate random
    numbers.

    Attributes:
        something


    """
    def __init__(self, random_seed: str, key_size: int = DEFAULT_KEY_LENGTH):
        """Initializes with random seed and optionally key length.

        Args:
            random_seed: the seed to feed in random generator if it's not int
            the hash value will be used.
            key_size: RSA key size in bits, have to be 1024, 2048 or 4096.
        """
        self._key_size = key_size
        self._random_source = random.SystemRandom(random_seed)
        # use the practically recommended public key
        self._e = PUBLIC_KEY
        # prime numbers p and q should be similar in size.
        self._p = 0
        while not self._miller_rabin(self._p) or (self._p-1) % self._e == 0:
            self._p = self._random_source.getrandbits(self._key_size // 2)
            self._p |= 1
            self._p |= 1 << (self._key_size // 2 - 1)
        self._q = 0
        while not self._miller_rabin(self._q) or (self._q-1) & self._e == 0\
                or self._q == self._p:
            self._q = self._random_source.getrandbits(self._key_size // 2)
            self._q |= 1
            self._q |= 1 << (self._key_size // 2 - 1)
        self._n = self._p * self._q
        # We use Carmichael's totient function in stead of the original Euler
        # totient function.  Since we generated p and q considering the public
        # key in advance, no need for coprimality test here.
        carmichael = (self._p-1) * (self._q-1) / math.gcd(self._p, self._p)
        # TODO: use extended Euclidean algorithm to obtain private key d

    def _miller_rabin(self,
                      n: int,
                      tolerance_power: int = FALSE_PRIME_TOLERANCE_POWER
                      ) -> bool:
        """Runs Miller-Rabin primality test on the input.

        Args:
            n: The candidate to test on.
            tolerance_power: If the possibility of the number passed test is
            composite is no grater
            than 2^tolerance_power we believe it's prime.

        Returns:
            Either n pass Miller-Rabin primality test or not.

        Raises:
            ValueError when inputs are invalid.
        """
        # step 0: input validation and short outs
        if tolerance_power >= 0:
            raise ValueError("tolerance_power should be negative.")
        if n < 0:
            raise ValueError("Test target is not positive.")
        if n & 1 == 0:
            return False
        # step 1: factor (n - 1) into 2^r * d where r and d are integers.
        d = n - 1
        r = 0
        while d & 1 == 0:
            r += 1
            d >>= 1
        # step 2: run the witness loop that repeat at most k times.
        k = (-tolerance_power + 1) // 2
        base_list = self._random_source.sample(range(2, n-1), min(k, n-3))
        for a in base_list:
            x = pow(a, d, n)
            if x == 1 or x == n-1:
                continue
            i = 1
            while i < r:
                x = pow(x, 2, n)
                if x == n-1:
                    break
            if i < r:
                continue
            return False
        return True

    def _extended_euclidean(self):
        pass


def main():
    key_generator = GenKey(sys.argv[1])
    pass


if __name__ == '__main__':
    main()
