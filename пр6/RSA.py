import random
from sympy import isprime


class RSACipher:
    def __init__(self):
        pass

    @staticmethod
    def __generate_prime_number(bitsize=1024):
        while True:
            p = random.getrandbits(bitsize)
            if isprime(p):
                return p

    @staticmethod
    def __mod_inverse(a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def generate_keys(self, bitsize=8):
        p = self.__generate_prime_number(bitsize)
        q = self.__generate_prime_number(bitsize)
        n = p * q
        phi_n = (p - 1) * (q - 1)

        c = random.randint(2, phi_n - 1)
        while isprime(c) == False or c % phi_n == 0:
            c = random.randint(2, phi_n - 1)

        d = self.__mod_inverse(c, phi_n)

        public_key = (c, n)
        private_key = (d, n)
        return public_key, private_key

    def encrypt(self, plain_text, public_key):
        c, n = public_key
        encrypted_text = ''.join(chr(pow(ord(char), c, n)) for char in plain_text)
        return encrypted_text

    def decrypt(self, encrypted_text, private_key):
        d, n = private_key
        decrypted_text = ''.join([chr(pow(ord(char), d, n)) for char in encrypted_text])
        return decrypted_text
