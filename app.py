import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)



@app.route("/")
def welcome():
    return """<html>
<h1>Hawaii Climate App (Flask API)</h1>
<p>Precipitation Analysis:</p>
<a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
<p>Station Analysis:</p>
<a href="/api/v1.0/stations">/api/v1.0/stations</a>
<p>Temperature Analysis:</p>
<a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
<p>Start Day Analysis:</p>
<a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a>
<p>Start & End Day Analysis:</p>
<a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a>
</html>
"""



@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= one_year_ago).\
            order_by(Measurement.date).all()

    precipitation_data_list = dict(precipitation_data)

    return jsonify(precipitation_data)



@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name).all()

    # station_list = list(stations)

    station_list = []
    for station in stations:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        station_list.append(station_dict)

    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= one_year_ago).\
            order_by(Measurement.date).all()

    tobs_list = list(tobs)

    return jsonify(tobs_list)



@app.route("/api/v1.0/<start>")
def start_day(start):
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            group_by(Measurement.date).all()

    start_day_list = list(start_day)

    return jsonify(start_day_list)



@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
    start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).\
            group_by(Measurement.date).all()
        
    start_end_day_list = list(start_end_day)

    return jsonify(start_end_day_list)



if __name__ == '__main__':
    app.run(debug=True)