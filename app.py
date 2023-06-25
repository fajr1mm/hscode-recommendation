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
    print(f'type query: {type(query)} ')
    keys = {"query": query}
    prediction = r.get("https://1a14-202-137-230-7.ngrok-free.app/lr-hs-recommendations", params=keys)
    results = prediction.json()
    limited_iterator = itertools.islice(iter(results.items()),10)
    item_list = list(limited_iterator)

    print('Query: ', query)
    print(results)
    print(item_list)

    return render_template('index.html', query=query, result=item_list)

if __name__ == '__main__':
    app.run(debug=True, port=8000)