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
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returning Precipitation"""
    # Query dates and precip
    results = session.query(Measurement.prcp, Measurement.date).all()

    # Convert list of tuples into normal list
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


@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point.
Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Query
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >='2016-08-23').all()
    tobs = list(np.ravel(tobs_results))
    return jsonify(tobs)

#books = sess.query(Book).filter(Book.title.like(likeString))


@app.route("/api/v1.0/<start>")
def s_start(start):
    """When given the start only, calculate TMIN, TAVG, and TMAX for all
     dates greater than and equal to the start date."""
    start_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    start1 = list(np.ravel(start_results))
    return jsonify(start1)

@app.route("/api/v1.0/<start>/<end>")
def s_start(start,end):
    """Lolz"""
    if end != None
    results_start_end = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    start_end = list(np.ravel(results_start_end))
    return jsonify(start_end)




if __name__ == '__main__':
    app.run(debug=True)
