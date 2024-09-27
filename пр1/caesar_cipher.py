from alphabets import ALPHABETS


class CaesarCipher:
    def __init__(self):
        self.text = ""
        self.__alphabet = None
        self.__alphabet_length = None
        self.__key = None

    def __set_alphabet(self, text):
        idx = 0
        letter = ""
        alphabet = ""

        while idx < len(text):
            if text[idx].isalpha():
                letter = text[idx]
                break
            idx += 1

        for i in range(len(ALPHABETS)):
            if letter.lower() in ALPHABETS[i]:
                alphabet = ALPHABETS[i]
                break
        else:
            raise ValueError("Мови тексту не знайдено!")

        for char in text:
            if char.isalpha() and char.lower() not in alphabet:
                raise ValueError("Всі літери тексту повинні бути однієї мови!")

        self.__alphabet = alphabet
        self.__alphabet_length = len(self.__alphabet)

    def __set_key(self, key):
        try:
            key = int(key)
        except ValueError:
            raise ValueError("Ключ повинен бути цілим числом!")
        if key <= 0 or key >= self.__alphabet_length:
            raise ValueError(f"Ключ повинен бути в межах від 1 до {self.__alphabet_length - 1}!")
        self.__key = key

    def encrypt(self, text, key):
        self.__set_alphabet(text)
        self.__set_key(key)
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                encrypted_char = self.__alphabet[
                                  (self.__alphabet.index(char.lower()) + self.__key) % self.__alphabet_length]
                if char.isupper():
                    encrypted_char = encrypted_char.upper()
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        self.text = encrypted_text
        return self.text

    def decrypt(self, text, key):
        self.__set_alphabet(text)
        self.__set_key(key)
        if self.text and text == self.text:
            decrypted_text = ""
            for char in text:
                if char.isalpha():
                    decrypted_char = self.__alphabet[(self.__alphabet.index(char.lower()) + self.__alphabet_length
                                      - self.__key % self.__alphabet_length) % self.__alphabet_length]
                    if char.isupper():
                        decrypted_char = decrypted_char.upper()
                    decrypted_text += decrypted_char
                else:
                    decrypted_text += char
            self.text = decrypted_text
        return self.text
