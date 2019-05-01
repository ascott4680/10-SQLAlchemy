import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returning Precipitation"""
    # Query dates and precip
    results = session.query(Measurement.prcp, Measurement.date).all()

    # Convert list of tuples into normal list
    #prcp = list(np.ravel(results))
    prcp_dict = []
    for result in results:
        prcp = {}
        prcp["precipitation"] = result.prcp
        prcp["date"] = result.date
        prcp_dict.append(prcp)
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Returning list of stations"""
    # Query all stations
    stations = session.query(Station.station).all()

    results = list(np.ravel(stations))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
