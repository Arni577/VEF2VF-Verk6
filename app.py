from flask import Flask, render_template as rnd
from requests import get

app = Flask(__name__)

with get("https://apis.is/petrol") as response:
	if response:
		data = response.json()["results"]
		ts = response.json()["timestampPriceChanges"]
	else:
		print("API error")
		exit()

tsSplit = ts.split("T")
tsDay = tsSplit[0]
tsHour = tsSplit[1][:8]


stations = []
for station in data:
    if station["company"] not in stations:
        stations.append(station["company"])

c_bensin = data[0]
c_disel = data[0]
for station in data:
	if station["bensin95"] < c_bensin["bensin95"]:
		c_bensin = station
	if station["diesel"] < c_disel["diesel"]:
		c_disel = station


@app.route("/")
def index():
	return rnd("index.html", stations=stations, tsDay=tsDay, tsHour=tsHour, data=data, c_bensin=c_bensin, c_disel=c_disel)

@app.route("/company/<name>")
def company(name):
	return rnd("company.html", name=name, data=data, tsDay=tsDay, tsHour=tsHour, c_bensin=c_bensin, c_disel=c_disel)

@app.route("/station/<key>")
def gas_station(key):
	for i in data:
		if i["key"] == key:
			station = i
			break
	return rnd("station.html", key=key, data=data, station=station, tsDay=tsDay, tsHour=tsHour, c_bensin=c_bensin, c_disel=c_disel)


@app.errorhandler(404)
def error404(error):
	return rnd('error.html', error_type=404, error=error)

if __name__ == "__main__":
	app.run(debug=True)
