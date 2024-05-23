from typing import List

from guessa_word_game import GuessResult, LetterMatchResult, LetterMatchedType


def create_letter_html (letter_result: LetterMatchResult):
    if letter_result.letter_matched_type == LetterMatchedType.CORRECT:
        return f"<font color='#83D67E' size='7'>{letter_result.letter}</font>"
    elif letter_result.letter_matched_type == LetterMatchedType.GOOD_BUT_WRONG_SPOT:
        return f"<font color='#C7C911' size='7'>{letter_result.letter}</font>"
    elif letter_result.letter_matched_type == LetterMatchedType.WRONG:
        return f"<font color='#8D0505' size='7'>{letter_result.letter}</font>"
    else:
        raise RuntimeError(f"Unknown LetterMatchedType:{letter_result.letter_matched_type}")


def create_boxed_letter(letter_result: LetterMatchResult):
    return f"<div style='padding: 10px; border: 2px solid; display: inline-block; width: 30px;'>{create_letter_html(letter_result)}</div>"


def create_guess_result_html(guess_result: GuessResult):
    return "".join(list(map(create_boxed_letter, guess_result.letter_result_list)))


def create_guess_result_list_html(guess_result_list: List[GuessResult]):
    return "<br>".join(list(map(create_guess_result_html, guess_result_list)))
