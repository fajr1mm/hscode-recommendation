from flask import Flask, render_template, request

app = Flask(__name__)

search_results = 'egg'
angka = "1234"
dictionary = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    return render_template('results.html',
                           query=query,
                           results=search_results,
                           angka = angka)


if __name__ == '__main__':
    app.run(debug=True, port=8000)