from typing import Tuple, List
from enum import Enum


class LetterMatchedType(Enum):
    CORRECT = 1
    GOOD_BUT_WRONG_SPOT = 2
    WRONG = 3
    UNDECIDED_YET = 4


class LetterMatchResult:
    def __init__(self, letter:str, letter_matched_type: LetterMatchedType):
        self.letter = letter
        self.letter_matched_type = letter_matched_type

    def get_match_info_letter(self):
        if self.letter_matched_type is LetterMatchedType.CORRECT:
            return "C"
        elif self.letter_matched_type is LetterMatchedType.GOOD_BUT_WRONG_SPOT:
            return "G"
        elif self.letter_matched_type is LetterMatchedType.WRONG:
            return "W"
        elif self.letter_matched_type is LetterMatchedType.UNDECIDED_YET:
            return "U"
        else:
            raise RuntimeError(f"Unrecognized enum:{self.letter=}, {self.letter_matched_type=}")

    def __repr__(self):
        return f"{self.letter}:{self.get_match_info_letter()}"


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

    def create_matching_info_str(self):
        return "".join([letter_result.get_match_info_letter() for letter_result in self.letter_result_list])

    @staticmethod
    def _create_letter_result_list(answer: str, guess: str) -> List[LetterMatchResult]:
        letter_result_list: List[LetterMatchResult] = []
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                letter_result_list.append(LetterMatchResult(guess[i], LetterMatchedType.CORRECT))
            else:
                letter_result_list.append(LetterMatchResult(guess[i], LetterMatchedType.UNDECIDED_YET))
        for i in range(len(guess)):
            if letter_result_list[i].letter_matched_type == LetterMatchedType.UNDECIDED_YET:
                if guess[i] in answer and GuessResult._char_isnt_noted_yet(guess[i], answer, letter_result_list):
                    letter_result_list[i].letter_matched_type = LetterMatchedType.GOOD_BUT_WRONG_SPOT
                else:
                    letter_result_list[i].letter_matched_type = LetterMatchedType.WRONG
        return letter_result_list

    @staticmethod
    def _char_isnt_noted_yet(char: str, answer: str, letter_result_list_so_far: List[LetterMatchResult]) -> bool:
        """returns True if all of this specific char in answer have not already been noted yet"""
        already_noted_count = 0
        for letter_result in letter_result_list_so_far:
            if letter_result.letter == char and (letter_result.letter_matched_type is LetterMatchedType.CORRECT or letter_result.letter_matched_type is LetterMatchedType.GOOD_BUT_WRONG_SPOT):
                already_noted_count += 1
        total = answer.count(char)
        if already_noted_count > total:
            raise RuntimeError(f"Should never have more noted than total for:{char=}, {answer=}, {letter_result_list_so_far=}, {already_noted_count=}. {total=}")
        elif already_noted_count == total:
            return False
        else:
            return True


class GameStatus(Enum):
    NOT_STARTED_YET = 1
    PLAYING = 2
    WON = 3
    LOST = 4


class GuessaWordGame:

    def __init__(self, word: str):
        self.word = word
        self.guess_results: List[GuessResult] = []
        self.all_incorrect = ""
        self.game_status: GameStatus = GameStatus.NOT_STARTED_YET

    def is_ready_to_play(self):
        return self.game_status is GameStatus.NOT_STARTED_YET or self.game_status is GameStatus.PLAYING

    def get_word_length(self):
        return len(self.word)

    def make_new_guess(self, guessed_word: str) -> None:
        new_result = GuessResult(self.word, guessed_word)
        for new_wrong in new_result.calc_all_wrong_letters():
            if new_wrong not in self.all_incorrect:
                self.all_incorrect += new_wrong
        self.guess_results.append(new_result)
        if self.game_status is GameStatus.NOT_STARTED_YET:
            self.game_status = GameStatus.PLAYING
        elif self.game_status is GameStatus.PLAYING:
            if self.guess_results[-1].is_solved():
                self.game_status = GameStatus.WON
            elif len(self.guess_results) >= 6:
                self.game_status = GameStatus.LOST

    def __str__(self) -> str:
        if self.guess_results:
            return f"{self.guess_results[-1]}, {self.all_incorrect=}"
        else:
            return "No guess yet"


def main():
    game = GuessaWordGame("sweet")
    user_input = ""
    while user_input != "quit" and game.is_ready_to_play():
        user_input = input("Enter your guess:")
        game.make_new_guess(user_input)
        print(game)
    print("you win!")


if __name__ == "__main__":
    main()
