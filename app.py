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