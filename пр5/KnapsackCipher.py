import random


class KnapsackCipher:
    def generate_keys(self, key_len):
        private_key = self.__generate_private_key(key_len)
        public_key = self.__generate_public_key(private_key)
        return  public_key, private_key

    def __generate_private_key(self, key_len):
        b = [random.randint(1, 10)]
        for _ in range(1, key_len):
            b.append(random.randint(sum(b) + 1, 2 * sum(b)))

        m = random.randint(sum(b) + 1, 2 * sum(b))
        t = random.randint(2, m - 1)
        while self._gcd(t, m) != 1:
            t = random.randint(2, m - 1)

        return {"b": b, "m": m, "t": t}

    @staticmethod
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def __generate_public_key(self, private_key):
        b, m, t = private_key["b"], private_key["m"], private_key["t"]
        return [(bi * t) % m for bi in b]

    def encrypt(self, message, public_key):
        binary_list = []
        for c in message:
            binary_list.append("0" * (len(public_key) - len(bin(ord(c))[2:])) + bin(ord(c))[2:])
        print(binary_list)
        result = []

        for i in range (len(binary_list)):
            result.append(0)
            for j in range(len(public_key)):
                result[i] += int(binary_list[i][j]) * public_key[j]
        return result

    def decrypt(self, cipher, private_key):
        result = ""
        b, m, t = private_key["b"], private_key["m"], private_key["t"]

        s = pow(t, -1, m)

        decrypted_binary = []
        for c in cipher:
            c_prime = (c * s) % m
            binary_representation = ""
            for bi in reversed(b):
                if bi <= c_prime:
                    binary_representation += "1"
                    c_prime -= bi
                else:
                    binary_representation += "0"
            decrypted_binary.append(binary_representation[::-1])
        for block in decrypted_binary:
            result += chr(int(block, 2))
        return result


def main():
    knapsack_cipher = KnapsackCipher()
    message = "hello world"
    public_key, private_key = knapsack_cipher.generate_keys(8)
    for i in range(len(message)):
        print(bin(ord(message[i])))
    cipher = knapsack_cipher.encrypt(message, public_key)
    print(cipher)
    print(knapsack_cipher.decrypt(cipher, private_key))


if __name__ == '__main__':
    main()
