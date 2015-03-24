from coreapp import app
import flask
from flask import Flask, render_template, request
from random import randint
import python.cipher as cf
import python.general as general
import pickle

#app = Flask(__name__)

@app.route('/')
def home():
    return render_template("cnc.html")


@app.route('/solve')
def solve():
    cipher = {}
    text = general.generate_paragraph()
    cipher['text'] = text
    cipher['cipher'] = cf.ceasar_shift_encode(text, randint(2,9))
    #pickle.dump(cipher, open('session.pkl', 'w'))
    return flask.jsonify(**cipher)

#if __name__ == '__main__':
#    app.run()

