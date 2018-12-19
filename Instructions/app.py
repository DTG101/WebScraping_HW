from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import pymongo
import Scraping_HW_PY

app = Flask(__name__)

#create connection variable

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template ("index.html", mars=mars)

@app.route("/scrape")
def scraper ():
    mars = mongo.db.mars
    mars_data = Scraping_HW_PY.scrape()
    mars.update({}, mars_data, upsert= True)
    return redirect ("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)