from typing import Tuple, List


class GuessResult:

    def __init__(self, answer, guess):
        self.answer = answer
        self.matched, self.correct_but_wrong_place, self.wrong = GuessResult._process_guess(answer, guess)

    def is_correct(self):
        return self.matched == self.answer

    def __str__(self) -> str:
        return f"{self.matched=}, {self.correct_but_wrong_place=}, {self.wrong=}"

    @staticmethod
    def _process_guess(answer, guess: str) -> Tuple[str, str, str]:
        matched = ""
        correct_but_wrong_place = ""
        wrong = ""
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                matched += answer[i]
                correct_but_wrong_place += "-"
            elif guess[i] in answer and GuessResult._char_isnt_noted_yet(guess[i], answer, matched, correct_but_wrong_place):
                matched += "-"
                correct_but_wrong_place += guess[i]
            else:
                matched += "-"
                correct_but_wrong_place += "-"
                wrong += guess[i]
        return matched, correct_but_wrong_place, wrong

    @staticmethod
    def _char_isnt_noted_yet(char: str, answer: str, matched: str, correct_but_wrong_place: str) -> bool:
        """returns True if all of this specific char in answer have already been noted in correct or wrong place"""
        already_noted_count: int = matched.count(char)+correct_but_wrong_place.count(char)
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
            return self.word == self.guess_results[-1].is_correct()
        else:
            return False

    def make_new_guess(self, guessed_word: str) -> None:
        new_result = GuessResult(self.word, guessed_word)
        for new_wrong in new_result.wrong:
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
