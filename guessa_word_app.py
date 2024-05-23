import random
from flask import Flask, request

import guess_word_html_creator
from guessa_word_game import GuessaWordGame, GuessResult
from word_data_source import find_words_with_lettercount, create_individual_word_count_map


app = Flask(__name__)
all_5_letter_words = find_words_with_lettercount(create_individual_word_count_map("data/english.txt"), 5)
my_game = GuessaWordGame(random.choice(all_5_letter_words))
# my_game = GuessaWordGame("lured")


@app.route("/", methods=["GET", "POST"])
def home():
    new_guess = request.form.get("guess", "")
    html = None
    if new_guess != "":
        my_game.make_new_guess(new_guess)
        html = guess_word_html_creator.create_guess_result_list_html(my_game.guess_results)
    if html:
        html += "<br>"
    else:
        html = "Make first guess<br>"
    guess_form = """
                <form action="/" method="POST">
                     <input type='text' name='guess'>
                     <input type='submit' value='Guess'>
                </form>
            """
    give_up_form = """
                    <form action="/giveup" method="POST">
                         <input type='submit' value='Give Up?'>
                    </form>
                """
    return html + guess_form + give_up_form


@app.route("/giveup", methods=["POST"])
def give_up():
    html = guess_word_html_creator.create_guess_result_list_html(my_game.guess_results)
    html += f"<br>Too bad. You made {len(my_game.guess_results)} guesses. The word was:<br>"
    html += guess_word_html_creator.create_guess_result_html(GuessResult(my_game.guess_results[-1].guess, my_game.word))
    return html


if __name__ == "__main__":
    app.run(host="localhost", debug=True)