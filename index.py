from flask import Flask, render_template, request
from random import randint
import cipher as cf
import general

app = Flask(__name__)

class Cipher():
	text = "" 
	cipher = ""

cipher = Cipher()

@app.route('/')
def home():
	return render_template("home.html")


@app.route('/solve')
def solve():
	text = general.generate_paragraph()
	cipher.text = text
	cipher.cipher = cf.ceasar_shift_encode(text, randint(2,9))	
	return render_template("solve.html", cipher=cipher.cipher)

@app.route('/solve/check/')
def check():
	solution = str(request.args.get("solution"))
	if(solution == cipher.text):
		return render_template("solve.html", cipher=cipher.cipher, solution="Your solution was correct!")	
	return render_template("solve.html", cipher=cipher.cipher, solution="Your solution was incorrect, Please try again.")

if __name__ == '__main__':
    app.run()

