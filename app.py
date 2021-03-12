import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br/>"
        f"Enter in the start_date and end_date information<br/>"
        f"Use YYYY-MM-DD for the date format"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query all precipitation data
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query all stations
    stations = session.query(Station.id, Station.name).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    station_info = []
    for id, name in stations:
        station_dict = {}
        station_dict["Station ID"] = id
        station_dict["Station Name"] = name
        station_info.append(station_dict)
    return jsonify(station_info)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query temperature observations (tobs)
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    most_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >=query_date).filter(Measurement.station =="USC00519281").all()
    session.close()
    
    # Create a dictionary from the row data and append to a list
    tobs_info = []
    for date, tobs in most_tobs:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temperature Observations'] = tobs
        tobs_info.append(tobs_dict)
    return jsonify(tobs_info)

if __name__ == '__main__':
    app.run(debug=True)