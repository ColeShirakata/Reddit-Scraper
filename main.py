from flask import Flask, render_template    

app = Flask(__name__)

@app.route("/")
def test(name=None):
    return render_template('index.html', name=name)

@app.route("/css")
def css():
    return render_template('styles.css')
