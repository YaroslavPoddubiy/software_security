from alphabets import ALPHABETS
from math import isqrt
from random import choice

class BookCipher:
    def __init__(self):
        self.text = ""
        self.__alphabet = None
        self.__alphabet_length = None
        self.__key = []

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
                raise ValueError("Всі літери повинні бути однієї мови!")

        self.__alphabet = alphabet
        self.__alphabet_length = len(self.__alphabet)

    def prepare_key(self, key):
        new_key = ""
        for char in key:
            if char.isalpha():
                if char.lower() not in self.__alphabet:
                    raise ValueError("Всі літери тексту повинні бути однієї мови!")
                new_key += char.lower()
        return new_key

    def __set_key(self, key):
        self.__key = []
        if len(key) >= 10000:
            rows = 100
        else:
            rows = isqrt(len(key))
        for i in range(rows):
            self.__key.append("")
            for j in range(rows):
                self.__key[i] += key[i * rows + j]
        print(key)

    def get_random_position(self, letter) -> str:
        positions = []
        for i, row in enumerate(self.__key):
            for j, char in enumerate(row):
                if char.lower() == letter.lower():
                    positions.append(f"{i}/{j}")

        return choice(positions)

    @staticmethod
    def parse_positions(positions_text):
        positions = positions_text.split(",")
        for i in range(len(positions)):
            row, column = positions[i].split("/")
            try:
                positions[i] = (int(row), int(column))
            except ValueError:
                raise ValueError("Дані для розшифрування мають бути у форматі INT/INT,INT/INT,...")
        return positions

    def encrypt(self, text, key):
        self.__set_alphabet(text)
        key = self.prepare_key(key)
        self.__set_key(key)
        if not all(letter.lower() in key[:int(len(self.__key) ** 2)] for letter in text if letter.isalpha()):
            self.__key = []
            raise ValueError("Цього тексту недостатньо для ключа")
        encrypted_text = ""
        for letter in text:
            if letter.isalpha():
                encrypted_text += self.get_random_position(letter) + ","
        return encrypted_text[:-1]

    def decrypt(self, text, key):
        self.__set_alphabet(key)
        key = self.prepare_key(key)
        self.__set_key(key)
        positions = self.parse_positions(text)

        decrypted_text = ""
        for position in positions:
            try:
                decrypted_text += self.__key[position[0]][position[1]]
            except IndexError:
                raise ValueError("Неможливо розшифрувати дані за допомогою цього ключа")

        return decrypted_text
