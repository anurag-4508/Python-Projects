from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here

    if request.method == 'POST':
        word = request.form.get('search')
    else:
        word = "welcome"

    result = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")

    try:
        data = result.json()
        return render_template('home.html', result=data,word=word)
    except Exception as e:
        if result.status_code == 404:
            return render_template("error.html",word=word)


if __name__ == '__main__':
    app.run(host='http://127.0.0.1:8000/',debug=True)
