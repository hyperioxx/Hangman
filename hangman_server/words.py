import random

WORDS = ['apple']


class Word:
    def __init__(self, word: str) -> None:
        self._word = word
        self._guessed = ["_"] * len(word)
        self._guesses = set()
        self._wrong_counter = 0

    def guess(self, char: str) -> bool:
        """guess takes a char and returns a boolean based on if the char is in the word.
        Also updated guessed word with new letters if applicable.

        :param char: char is a guessed character 
        :type char: str
        :return: if char in current word
        :rtype: bool
        """
        self._guesses.add(char)
        indexes = self.find_indexes(char)
        for i in indexes: self._guessed[i] = char
        
        if indexes:
            return True
        else:
            self._wrong_counter += 1  # TODO counts duplicate guesses
            return False

    def guess_word(self, word: str) -> bool:
        if self._word == word:
            return True
        return False

    def find_indexes(self, char: str) -> list:
        return [c for c, ltr in enumerate(self._word) if ltr == char]

    def __repr__(self) -> str:
        return  f"WORD: {''.join(self._guessed)} - Guesses: {', '.join(self._guesses)}"

    @property
    def incorrect_guesses_count(self) -> int:
        """ returns number of gueseses taken

        :return: guesses count
        :rtype: int
        """
        return self._wrong_counter

class WordFactory:
    
    @staticmethod
    def build() -> Word:
        new_word = random.choice(WORDS)
        return Word(new_word)