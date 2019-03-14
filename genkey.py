"""This script generate RSA public and private keys. Running this script
directly from shell should provide one argument <name>.
"""
import sys
import random
import json


DEFAULT_KEY_LENGTH = 2048
FALSE_PRIME_TOLERANCE_POWER = -128
PUBLIC_KEY = 65537


def extended_euclidean(a: int, b: int) -> (int, int):
    """The extended euclidean algorithm. Could be used to find gcd or
    modular multiplicative inverse if exist.

    ax + by = gcd(a, b)

    Args:
        a: The grater number of input.
        b: The smaller number of input.

    Return:
        r: GCD(a, b).
        t: Bezout's coefficient of b. If a and b are coprime it's equal to the
        modular inverse of a mod b.

    Raises:
        ValueError when a < b, b == 0 or any of them is negative.
    """
    if b == 0:
        raise ValueError("Input b can't be 0.", b)
    if a < 0 or b < 0:
        raise ValueError("Neither input can be negative.", a, b)
    if a < b:
        raise ValueError("Input a should be grater than b.", a, b)
    t = 0
    new_t = 1
    r = a
    new_r = b
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    t = t if t > 0 else t + a
    return r, t


class GenKey(object):
    """RSA key pair generator. Using sys.SystemRandom() to generate random
    numbers.

    Attributes:
        owner: key's owner's name
        key_size: key's size in bits, to be more specific, it's n's size.
        n: modulus for both private and public key
        e: public exponent.
        d: private exponent.

    """
    def __init__(self, owner: str, key_size: int = DEFAULT_KEY_LENGTH):
        """Initializes with random seed and optionally key length.

        Args:
            owner: owner's name of the key pair, it's hash value is also used
            as random seed.
            key_size: RSA key size in bits, have to be 1024, 2048 or 4096.
        """
        self.owner = owner
        self.key_size = key_size
        self._random_source = random.SystemRandom(owner)
        # use the practically recommended public key
        self.e = PUBLIC_KEY

        # prime numbers p and q should be similar in size.
        self._p = 0
        while not self._miller_rabin(self._p) or (self._p-1) % self.e == 0:
            self._p = self._random_source.getrandbits(self.key_size // 2)
            self._p |= 1
            self._p |= 1 << (self.key_size // 2 - 1)

        self._q = 0
        while not self._miller_rabin(self._q) or (self._q-1) & self.e == 0\
                or self._q == self._p:
            self._q = self._random_source.getrandbits(self.key_size // 2)
            self._q |= 1
            self._q |= 1 << (self.key_size // 2 - 1)

        self.n = self._p * self._q

        # We use Carmichael's totient function in stead of the original Euler
        # totient function.  Since we generated p and q considering the public
        # key in advance, no need for coprimality test here.
        if self._p < self._q:
            self._p, self._q = self._q, self._p
        gcd, _ = extended_euclidean(self._p-1, self._q-1)
        self._carmichael = (self._p-1) * (self._q-1) // gcd

        # Use extended Euclidean algorithm to obtain private key d
        _, self.d = extended_euclidean(self._carmichael, self.e)

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
            raise ValueError("tolerance_power should be negative.",
                             tolerance_power)
        if n < 0:
            raise ValueError("Test target is not positive.", n)
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
        # instead of selecting random k distinct numbers from the range [2, n-1)
        # we simply try k times for performance reasons
        for _ in range(k):
            a = self._random_source.randrange(2, n-1)
            x = pow(a, d, n)
            if x == 1 or x == n-1:
                continue
            i = 1
            while i < r:
                x = pow(x, 2, n)
                if x == n-1:
                    break
                i += 1
            if i < r:
                continue
            return False
        return True

    def export_keys(self):
        """Simply export public and private keys to <owner>.pub and <owner>.prv.
        For simplicity we just use json format. (Warned you. It's not secure!!!)
        """
        with open("{}.pub".format(self.owner), "w") as public_key_file:
            public_key = {"n": self.n, "e": self.e}
            json.dump(public_key, public_key_file)

        with open("{}.prv".format(self.owner), "w") as private_key_file:
            private_key = {"n": self.n, "d": self.d}
            json.dump(private_key, private_key_file)


def main():
    """Creates a GenKey object and export the keys"""
    key_generator = GenKey(sys.argv[1])
    key_generator.export_keys()


if __name__ == '__main__':
    main()
