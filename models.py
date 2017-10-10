import datetime
import os
import peewee
import sys
from playhouse.db_url import connect
from playhouse.postgres_ext import JSONField
from geoip import open_database

match = geolite2.lookup('17.0.0.1')
match is not None



DB = connect(
  os.environ.get(
    'DATABASE_URL',
    'postgres://localhost:5432/weather' #5432 is the default port for databases
  )
)

class BaseModel (peewee.Model):
  class Meta:
    database = DB

class weathertable (BaseModel):
  cityname = peewee.CharField(max_length=60)
  stampcreated = peewee.DateTimeField(default=datetime.datetime.utcnow)
  weatherdata = JSONField()

  def __str__ (self):
    return self.name
