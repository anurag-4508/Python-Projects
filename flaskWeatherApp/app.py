import urllib.request

from flask import Flask, render_template, url_for, redirect, request
from forms import SearchForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "8fc58bd0106ea102"


@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['search']
    else:
        city = 'mathura'

    params = {
        "access_key": "c53ad3ab0d0435ce4a6f59126e421c08",
        "query": city
    }

    # source contain json data from api
    raw_source = requests.get('http://api.weatherstack.com/current', params)
    source = raw_source.json()

    # if raw_source.ok:
    #     return render_template('home.html', result=source)
    # else:
    #     return render_template('errors.html')

    try:
        return render_template('home.html', result=source)
    except Exception as e:
        if e == "'dict object' has no attribute 'location'":
            return render_template('errors.html', error="The city you are trying to access is not in database")
        else:
            return render_template('errors.html', error=e)


if __name__ == '__main__':
    app.run(debug=True)
