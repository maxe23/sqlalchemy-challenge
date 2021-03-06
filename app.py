import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (f"Available Routes: <br/>"
    f"/api/v1.0/precipitation<br/>"
    f"- Precipitation results by date <br/>"
    f"/api/v1.0/stations<br/>"
    f"- Weather Stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"-Temperature Observations<br/>"
    f"/api/v1.0/<start><br/>"
    f"- Given the start date (YYYY-MM-DD) returns the min, max, and avg temps for days after the given start date<br/>"
    f"/api/v1.0/<start>/<end><br/>"
    f"- Given a start and end date (YYYY-MM-DD) returns the min, max, and avg temps for dates between the given start and end date<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    year = dt.date(2017,8,23) - dt.timedelta(days=365)

    p_year = session.query(measurement.date, (measurement.prcp)).\
                    filter(measurement.date >= year).all()

    rain_totals = []
    for row in p_year:
        row = {}
        row['date'] = p_year[0]
        row['pcrp'] = p_year[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= year).all()
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start():
    date = input(f'Choose a start date (YYYY-MM-DD): ')
    start_temp = session.query(measurement.date, measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= {date}).all()
    return jsonify(start_temp)

@app.route("/api/v1.0/<start><end>")
def end():
    s_date = input(f'Choose a start date (YYYY-MM-DD): ')
    e_date = input(f'Choose an end date (YYYY-MM-DD): ')
    start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.station).all().\
            filter(measurement.date >= {s_date}, (measurement.date <= {e_date})).all()
    return jsonify({'error': f'Date range {start} not found.'})

if __name__ == "__main__":
    app.run(debug=True)