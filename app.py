from flask import Flask, render_template, request
import requests as r
import itertools
from preprocessing import preprocess
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])

def search():
    query = request.form['query']
    query = preprocess(query)
    keys = {"query": query}
    prediction = r.get("https://9a12-36-67-214-133.ngrok-free.app/lr-hs-recommendations", params=keys)
    results = prediction.json()
    limited_iterator = itertools.islice(iter(results.items()),10)
    item_list = list(limited_iterator)

    print('Query: ', query)

    return render_template('results.html', query=query, result=item_list)

if __name__ == '__main__':
    app.run(debug=True, port=8000)