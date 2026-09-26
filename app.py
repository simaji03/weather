from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "f82056ef99264554931170008251011"   #your weatherapi key

#f82056ef99264554931170008251010
@app.route("/", methods=["GET", "POST"])
def index():
    city = "Nadiad"
    if request.method == "POST":
        city = request.form["city"]

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=10&aqi=no&alerts=no"
    res = requests.get(url).json()
    """ print("City searched:", city)
    print("Response from API:", res) """

    if "current" not in res:
        return render_template("index.html", error="City not found or API limit reached")

    weather = {
        "city": res["location"]["name"],
        "country": res["location"]["country"],
        "temp_c": res["current"]["temp_c"],
        "feelslike_c": res["current"]["feelslike_c"],
        "condition": res["current"]["condition"]["text"],
        "icon": res["current"]["condition"]["icon"],
        "humidity": res["current"]["humidity"],
        "wind_kph": res["current"]["wind_kph"],
        "pressure_mb": res["current"]["pressure_mb"],
        "precip_mm": res["current"]["precip_mm"],
        "vis_km": res["current"]["vis_km"],
        "uv": res["current"]["uv"]
    }
        # Get hourly forecast (first 6 hours)
    forecast_hours = res["forecast"]["forecastday"][0]["hour"][:6]

    hours_data = []
    for hour in forecast_hours:
        hours_data.append({
            "time": hour["time"].split(" ")[1],  # only show time part
            "temp_c": hour["temp_c"],
            "icon": hour["condition"]["icon"]
        })

       # Get 10-day forecast
    forecast_days = res["forecast"]["forecastday"]
    days_data = []
    for d in forecast_days:
        days_data.append({
            "date": d["date"],
            "avg_temp": d["day"]["avgtemp_c"],
            "icon": d["day"]["condition"]["icon"]
        })

    return render_template("index.html", weather=weather, hours=hours_data, days=days_data)




if __name__ == "__main__":
    app.run(debug=True)
