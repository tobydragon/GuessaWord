from typing import Tuple, List
from enum import Enum


class LetterMatchedType(Enum):
    CORRECT = 1
    GOOD_BUT_WRONG_SPOT = 2
    WRONG = 3


class LetterMatchResult:
    def __init__(self, letter:str, letter_matched_type: LetterMatchedType):
        self.letter = letter
        self.letter_matched_type = letter_matched_type


class GuessResult:

    def __init__(self, answer, guess):
        self.answer = answer
        self.guess = guess
        self.letter_result_list = GuessResult._create_letter_result_list(answer, guess)

    def is_solved(self):
        if len(self.letter_result_list) == len(self.answer):
            for letter_result in self.letter_result_list:
                if letter_result.letter_matched_type != LetterMatchedType.CORRECT:
                    return False
            return True

    def calc_all_wrong_letters(self) -> str:
        return "".join([letter_result.letter for letter_result in self.letter_result_list if letter_result.letter_matched_type == LetterMatchedType.WRONG])

    @staticmethod
    def _create_letter_result_list(answer: str, guess: str) -> List[LetterMatchResult]:
        letter_result_list: List[LetterMatchResult] = []
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                letter_result_list.append(LetterMatchResult(guess[i], LetterMatchedType.CORRECT))
            elif guess[i] in answer and GuessResult._char_isnt_noted_yet(guess[i], answer, letter_result_list):
                letter_result_list.append(LetterMatchResult(guess[i], LetterMatchedType.GOOD_BUT_WRONG_SPOT))
            else:
                letter_result_list.append(LetterMatchResult(guess[i], LetterMatchedType.WRONG))
        return letter_result_list

    @staticmethod
    def _char_isnt_noted_yet(char: str, answer, letter_result_list_so_far) -> bool:
        """returns True if all of this specific char in answer have not already been noted yet"""
        already_noted_count = 0
        for letter_result in letter_result_list_so_far:
            if letter_result.letter == char and letter_result.letter_matched_type != LetterMatchedType.WRONG:
                already_noted_count += 1
        # len([letter_result for letter_result in letter_result_list_so_far if letter_result.letter == char and letter_result.letter_matched_type != LetterMatchedType.WRONG ])
        # len(list(filter(lambda letter_result: letter_result.letter == char and letter_result.letter_matched_type != LetterMatchedType.WRONG, letter_result_list_so_far)))

        total: int = answer.count(char)
        if already_noted_count > total:
            raise RuntimeError("Should never have more noted than total")
        elif already_noted_count == total:
            return False
        else:
            return True


class GuessaWordGame:

    def __init__(self, word: str):
        self.word = word
        self.guess_results: List[GuessResult] = []
        self.all_incorrect = ""

    def is_finished(self) -> bool:
        if self.guess_results:
            return self.guess_results[-1].is_solved()
        else:
            return False

    def get_last_result(self):
        if self.guess_results:
            return self.guess_results[-1]
        else:
            return None

    def make_new_guess(self, guessed_word: str) -> None:
        new_result = GuessResult(self.word, guessed_word)
        for new_wrong in new_result.calc_all_wrong_letters():
            if new_wrong not in self.all_incorrect:
                self.all_incorrect += new_wrong
        self.guess_results.append(new_result)

    def __str__(self) -> str:
        if self.guess_results:
            return f"{self.guess_results[-1]}, {self.all_incorrect=}"
        else:
            return "No guess yet"


def main():
    game = GuessaWordGame("sweet")
    user_input = ""
    while user_input != "quit" and not game.is_finished():
        user_input = input("Enter your guess:")
        game.make_new_guess(user_input)
        print(game)
    print("you win!")


if __name__ == "__main__":
    main()
