from geo.geomodel import GeoModel
from google.appengine.ext import db

class DataPoint(GeoModel):
  weight = db.IntegerProperty()
  range = db.IntegerProperty()

class NewDataPoint(GeoModel):
  weight = db.IntegerProperty()
  range = db.IntegerProperty()
