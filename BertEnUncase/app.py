from flask import Flask, render_template, request, redirect, url_for, session
from search import search
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"
run_with_ngrok(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/data")
def data():
	return render_template("data.html")

@app.route("/recom")
def recom():
	return render_template("recom.html")

@app.route("/search", methods=["POST", "GET"])
def searchr():
	if request.method == "POST":
		query = request.form["query"]
		results = search(query, num_results=1000)
		session["results"] = results
		session["query"] = query
		return redirect(url_for("searchr"))
	return render_template("search.html", results=session["results"], query=session["query"])


if __name__ == '__main__':
	app.run()