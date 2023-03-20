import pandas as pd 
from flask import Flask, render_template, request, redirect, url_for, make_response
import os.path

app = Flask(__name__, template_folder="templates")


if not os.path.exists('polls.csv'):
    structure = {
        'pid': [],
        'poll': [],
        'option1': [],
        'option2': [],
        'option3': [],
        'votes1': [],
        'votes2': [],
        'votes3': []
    }

    pd.DataFrame(structure).set_index('pid').to_csv('polls.csv')


polls_df = pd.read_csv('polls.csv').set_index("pid")

@app.route("/")
def index():
    return render_template("index.html", polls=polls_df)

@app.route("/poll/<pid>")
def polls(pid):
    poll = polls_df.loc[int(pid)]
    return render_template('show_poll.html', poll=poll)

@app.route("/poll", methods=['GET', 'POST'])
def create_poll():
    if request.method == "GET":
        return render_template('new_poll.html')
    elif request.method == "POST":
        poll = request.form['poll']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']

        polls_df.loc[max(polls_df.index.values) + 1] = [poll, option1, option2, option3, 0, 0, 0]
        polls_df.to_csv('polls.csv')
        return render_template('index.html', polls=polls_df)

        

@app.route('/vote/<pid>/<option>')
def vote(pid, option):
    if request.cookies.get(f"vote_{pid}_cookie") is None:
        polls_df.at[int(pid), "votes"+str(option)] += 1
        polls_df.to_csv("polls.csv")
        response = make_response(redirect(url_for('polls', pid=pid)))
        response.set_cookie(f'vote_{pid}_cookie', str(option))
        return response
    else:
        return "Cannot vote more than once"


if __name__=="__main__":
    app.run(host="localhost", debug=True)

