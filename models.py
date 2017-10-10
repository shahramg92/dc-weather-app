import datetime
import os
import peewee
import sys
from playhouse.db_url import connect


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
  stampcreated = peewee.CharField(max_length=60)
  weatherdata = peewee.jsonField()

  def __str__ (self):
    return self.name
