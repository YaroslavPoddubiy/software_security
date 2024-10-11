from alphabets import ALPHABETS


class TrithemiusCipher:
    def __init__(self):
        self.text = ""
        self.__alphabet = None
        self.__alphabet_length = None
        self.__keys = []

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

    def __set_keys(self, keys):
        keys = list(keys)
        if len(keys) < 1 or len(keys) > 3:
            raise ValueError("Введіть ключ!")
        if len(keys) == 1:
            if not keys[0].isnumeric():
                keys[0] = keys[0].lower()
                if not all(char in self.__alphabet for char in keys[0] if char.isalpha()):
                    raise ValueError("Всі літери гасла повинні належати одному алфавіту!")
                else:
                    self.__keys = (keys[0], )
                    return
        try:
            for i in range(len(keys)):
                keys[i] = int(keys[i])
        except ValueError:
            raise ValueError("Ключ повинен бути цілим числом!")
        self.__keys = list(keys)

    def gain_key(self, position):
        if len(self.__keys) == 1 and isinstance(self.__keys[0], str):
            if self.__keys[0][position % len(self.__keys[0])] in (" ", "\r", "\t", "\n"):
                return 0
            return self.__alphabet.index(self.__keys[0][position % len(self.__keys[0])])
        key = 0
        for i in range(len(self.__keys)):
            key += self.__keys[-i-1] * pow(position, i)
        return key

    def encrypt(self, text, keys):
        self.__set_alphabet(text)
        self.__set_keys(keys)
        encrypted_text = ""
        for i in range(len(text)):
            if text[i].isalpha():
                key = self.gain_key(i)
                encrypted_char = self.__alphabet[
                                  (self.__alphabet.index(text[i].lower()) + key) % self.__alphabet_length]
                if text[i].isupper():
                    encrypted_char = encrypted_char.upper()
                encrypted_text += encrypted_char
            else:
                encrypted_text += text[i]
        self.text = encrypted_text
        return self.text

    def decrypt(self, text, keys):
        self.__set_alphabet(text)
        self.__set_keys(keys)
        if self.text and text == self.text:
            decrypted_text = ""
            for i in range(len(text)):
                key = self.gain_key(i)
                if text[i].isalpha():
                    decrypted_char = self.__alphabet[(self.__alphabet.index(text[i].lower()) + self.__alphabet_length
                                      - key % self.__alphabet_length) % self.__alphabet_length]
                    if text[i].isupper():
                        decrypted_char = decrypted_char.upper()
                    decrypted_text += decrypted_char
                else:
                    decrypted_text += text[i]
            self.text = decrypted_text
        return self.text
