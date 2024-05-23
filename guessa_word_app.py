import random
from flask import Flask, request

import guess_word_html_creator
from guessa_word_game import GuessaWordGame, GuessResult, GameStatus
from word_data_source import find_words_with_lettercount, create_individual_word_count_map


app = Flask(__name__)
all_5_letter_words = find_words_with_lettercount(create_individual_word_count_map("data/english.txt"), 5)
my_game = GuessaWordGame(random.choice(all_5_letter_words))
# my_game = GuessaWordGame("sigma")


@app.route("/", methods=["GET", "POST"])
def home():
    new_guess = request.form.get("guess", "")
    if new_guess != "":
        if my_game.get_word_length() == len(new_guess):
            my_game.make_new_guess(new_guess)

    if my_game.game_status is GameStatus.NOT_STARTED_YET:
        html = "Make first guess<br>" + guess_word_html_creator.create_guess_and_give_forms()
    else:
        html = guess_word_html_creator.create_guess_result_list_html(my_game.guess_results) + "<br>"
        if my_game.game_status is GameStatus.WON:
            html += "<font size=12> You Win!!!</font>"
        elif my_game.game_status is GameStatus.LOST:
            html += "<font size=12> Too many guesses, You Lose, but you can keep trying!!!</font>"
            html += guess_word_html_creator.create_guess_and_give_forms()
        else:
            html += guess_word_html_creator.create_guess_and_give_forms()
    return html


@app.route("/giveup", methods=["POST"])
def give_up():
    html = guess_word_html_creator.create_guess_result_list_html(my_game.guess_results)
    html += f"<br>Too bad. You made {len(my_game.guess_results)} guesses. The word was:<br>"
    html += guess_word_html_creator.create_guess_result_html(GuessResult(my_game.guess_results[-1].guess, my_game.word))
    return html


if __name__ == "__main__":
    app.run(host="localhost", debug=True)