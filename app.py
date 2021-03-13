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
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
        f"<br/>"
        f"Enter in the start_date and end_date information<br/>"
        f"Use YYYY-MM-DD for the date format<br/>"
        f"Use a forward slash ( / ) in the web browser to separate the start and end dates"
    )

#################################################
# Flask Routes
#################################################

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
        tobs_dict['Temperature (F)'] = tobs
        tobs_info.append(tobs_dict)
    return jsonify(tobs_info)

@app.route("/api/v1.0/<start_date>")
def solo_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query min/max/avg tobs from a start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()  
    session.close()

    # Create a dictionary for min/max/avg tobs
    date_list = []
    for min, avg, max in results:
        date_list_dict = {}
        date_list_dict["Min. Temp (F)"] = min
        date_list_dict["Avg. Temp (F)"] = avg
        date_list_dict["Max Temp (F)"] = max
        date_list.append(date_list_dict) 
    return jsonify(date_list, f"Date Selected: {start_date}")

@app.route("/api/v1.0/<start_date>/<end_date>")
def two_dates(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query min/max/avg tobs from a start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()  

    # Create a dictionary for min/max/avg tobs between the two dates
    two_date_list = []
    for min, avg, max in results:
        two_date_dict = {}
        two_date_dict["Min. Temp (F)"] = min
        two_date_dict["Avg. Temp (F)"] = avg
        two_date_dict["Max Temp (F)"] = max
        two_date_list.append(two_date_dict) 
    return jsonify(two_date_list, f"Dates Selected: {start_date} - {end_date}")
    

if __name__ == '__main__':
    app.run(debug=True)