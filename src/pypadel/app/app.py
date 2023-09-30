from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter-match')
def enter_match():
    return render_template('enter-match.html')

@app.route('/process-live-match', methods=['GET', 'POST'])
def process_live_match():
    if request.method == 'POST':
        # Extract form data
        date = request.form['date']
        tournament = request.form['tournament']
        round = request.form['round']
        player1 = request.form['player1']
        player2 = request.form['player2']
        player3 = request.form['player3']
        player4 = request.form['player4']
        type = request.form['type']
        category = request.form['category']
        advGame = request.form['advGame']

        # Redirect to the next page with the form data
        return redirect(url_for('input_live_match', date=date, tournament=tournament, round=round, player1=player1, player2=player2, player3=player3, player4=player4, type=type, category=category, advGame=advGame))
    else:
        # Render the process-live-match.html template when a GET request is made
        return render_template('process-live-match.html')


@app.route('/input-live-match', methods=['GET'])
def input_live_match():
    # Extract data from the URL
    date = request.args.get('date')
    tournament = request.args.get('tournament')
    round = request.args.get('round')
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')
    player3 = request.args.get('player3')
    player4 = request.args.get('player4')
    type = request.args.get('type')
    category = request.args.get('category')
    advGame = request.args.get('advGame')

    # Render the template with the data
    return render_template('input-live-match.html', date=date, tournament=tournament, round=round, player1=player1, player2=player2, player3=player3, player4=player4, type=type, category=category, advGame=advGame)


if __name__ == '__main__':
    app.run(debug=True)
