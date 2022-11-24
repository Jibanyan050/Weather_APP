from flask import Blueprint, render_template, request, redirect
from app.models import db, Result
import requests
from datetime import datetime

ui_bp = Blueprint(
  'ui_bp', __name__,
  template_folder='templates',
  static_folder='static'
)
# App Home Page


@ui_bp.route('/')
def home():
    return render_template("home.html")
# Results page


@ui_bp.route('/results')
def list_results():
    results = Result.query
    return render_template('results.html', results=results)


@ui_bp.route('/api/results')
def results_all():

    return {'data': [result.to_dict() for result in Result.query]}


@ui_bp.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = "a211d843be75bf396adc6de675116830"
    if temp_units == "F":
        data = get_weather_results_imperial(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])

    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    icon_url = "http://openweathermap.org/img/w/" + icon + ".png"
    timestamp = 1
    print(timestamp)
    dt_obj = datetime.utcfromtimestamp(timestamp)
    dt = datetime.utcfromtimestamp(timestamp)
    results = Result(location=location, weather=weather, datetime=dt)
    db.session.add(results)
    db.session.commit()

    return render_template('results.html',
      location=location, temp=temp, icon_url=icon_url, dt_obj=dt_obj, dt=dt,
      feels_like=feels_like, weather=weather, temp_units=temp_units, icon=icon)


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()
