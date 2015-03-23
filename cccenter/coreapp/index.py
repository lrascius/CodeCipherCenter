from flask import Flask, render_template, request
from random import randint
import python.cipher as cf
import python.general
import pickle

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("cnc.html")


@app.route('/solve')
def solve():
	text = general.generate_paragraph()
	cipher.text = text
	cipher.cipher = cf.ceasar_shift_encode(text, randint(2,9))	
	pickle.dump(obj, open('session.pkl', 'w'))
	return flask.jasonify(cipher.cipher)

if __name__ == '__main__':
    app.run()

