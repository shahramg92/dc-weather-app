import models

def forward ():
  models.DB.create_tables([models.weathertable])

if __name__ == '__main__':
  forward()
