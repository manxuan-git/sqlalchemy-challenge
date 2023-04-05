import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask 
app = Flask(__name__)


# routes
@app.route("/")
def home():
    return(
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"    
        f"/api/v1.0/tobs"    
        f"/api/v1.0/<start>"    
        f"/api/v1.0/<start>/<end>"    
    )   

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precipitation = {date:prcp for date, prcp in results}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session.query(func.count(Station.station)).all()
    stationlist = list(np.ravel(results))
    return jsonify(stationlist)

@app.route("/api/v1.0/tobs")
def temperatures():
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    temperaturelist = list(np.ravel(results))
    return jsonify(temperaturelist)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def datestats(start=None, end=None):

    select = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs]
              
    if not end:
        startDate = dt.datetime.strptime(start,"%m%d%Y%")
        results = session.query(*select).filter(Measurement.date >= startDate).all()
        temperaturelist = list(np.ravel(results))
        return jsonify(temperaturelist)

    else:
        startDate = dt.datetime.strptime(start,"%m%d%Y%")
        endDate = dt.datetime.strptime(end,"%m%d%Y%")
        results = session.query(*select).filter(Measurement.date >= startDate).filter(Measurement.date <= endDate).all()
        temperaturelist = list(np.ravel(results))   
        return jsonify(temperaturelist)
        

if __name__ == '__main__':
    app.run(debug=True)