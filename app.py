# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)

Base = automap_base()

# reflect an existing database into a new model
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
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
    return(
        f"Welcome to the Hawaii Weather API!<br/>"
        f"/api/v1.0/precipatation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipatation")
def precipatation():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date).all()
    precipatation_results = []
    for prcp in results:
        preciptation_dict = {}
        preciptation_dict["date"] = prcp.date
        preciptation_dict["prcp"] = prcp.prcp
        
        precipatation_results.append(preciptation_dict)
    return jsonify(precipatation_results)

@app.route("/api/v1.0/stations")
def stations():
    sel = [Measurement.station,
        func.count(Measurement.station)]
    station_query = session.query(* sel).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    station_results = []
    for stn in station_query:
        station_dict = {}
        station_dict['station'] = stn.station
        station_dict['count'] = stn.count
        
        station_results.append(station_dict)
    return jsonify(station_query)

@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sel = [Measurement.tobs]
    temp_results = session.query(*sel).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.station == "USC00519281").all()
    temperature_results = []
    for temp in temp_results:
        temp_dict = {}
        temp_dict['tobs'] = temp.tobs
        
        temperature_results.append(temp_dict)
    
if __name__ == "__main__":
    app.run(debug=True)