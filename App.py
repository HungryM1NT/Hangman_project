from flask import Flask, render_template, request, redirect

app = Flask(__name__)
difficulty = None
current_word = None
current_hint = ""
user_word = None
user_word_list = None
up_symbols = None
mid_symbols = None
down_symbols = None
result = None
stage = None
attempts_used = None


def stage_up(d):
    global stage
    if d == 1:
        stage += 1
    elif d == 2:
        if stage == 1:
            stage += 2
        else:
            stage += 1
    elif d == 3:
        if stage == 1 or stage == 3:
            stage += 2
        else:
            stage += 1
    elif d == 4:
        stage += 2
    elif d == 5:
        stage += 3


@app.route('/', methods=['POST', 'GET'])
def main():
    global difficulty
    global current_word
    global current_hint
    global user_word
    global user_word_list
    global up_symbols
    global mid_symbols
    global down_symbols
    global stage
    global attempts_used
    attempts_used = 0
    up_symbols = list('QWERTYUIOP')
    mid_symbols = list('ASDFGHJKL')
    down_symbols = list('ZXCVBNM')
    if request.method == 'POST':
        if request.form.get('slider'):
            difficulty = int(request.form.get('slider'))
            return render_template('word_selector.html')
        elif request.form.get('current_word'):
            text = request.form.get('current_word')
            for i in text:
                if ord('A') > ord(i) or ord('z') < ord(i) or ord('[') <= ord(i) <= ord('`'):
                    word_error = "Invalid word"
                    return render_template('word_selector.html', word_error=word_error)
            user_word = text.upper()
            current_word = list(user_word)
            if request.form.get('current_hint'):
                current_hint = request.form.get('current_hint')
                for i in current_hint:
                    if ord('A') > ord(i) or ord('z') < ord(i) or ord('[') <= ord(i) <= ord('`'):
                        hint_error = "Invalid hint"
                        return render_template('word_selector.html', hint_error=hint_error)
            user_word_list = ['_'] * len(current_word)
            stage = 1
            return redirect("/game")
        else:
            word_error = "Invalid word"
            return render_template('word_selector.html', word_error=word_error)
    return render_template('main.html')


@app.route('/game', methods=['POST', 'GET'])
def game():
    global up_symbols
    global mid_symbols
    global down_symbols
    global result
    global stage
    global difficulty
    global attempts_used
    if request.method == 'POST':
        current_symbol = request.form.get('button')

        if current_symbol in current_word:
            volume = current_word.count(current_symbol)
            for i in range(volume):
                symbol_index = ''.join(current_word).find(current_symbol)
                user_word_list[symbol_index] = current_symbol
                current_word[symbol_index] = '_'
        else:
            stage_up(difficulty)
            attempts_used += 1

        if stage == 7:
            result = 'You lose'
            return redirect("/end")
        elif current_word.count('_') == len(current_word):
            result = 'You win'
            return redirect("/end")

        if current_symbol in up_symbols:
            up_symbols.remove(current_symbol)
        elif current_symbol in mid_symbols:
            mid_symbols.remove(current_symbol)
        else:
            down_symbols.remove(current_symbol)
    return render_template('game.html', stage=stage,
                           user_word=' '.join(user_word_list),
                           current_hint=current_hint,
                           up_symbols=up_symbols,
                           mid_symbols=mid_symbols,
                           down_symbols=down_symbols,
                           attempts_used=attempts_used,
                           attempts=7-difficulty)


@app.route('/end', methods=['POST', 'GET'])
def end():
    global result
    global user_word
    if request.method == 'POST':
        return redirect("/")
    return render_template('end.html', stage=stage, result=result, word=user_word)

app.run()
