#!/usr/bin/env python3
import os
import tornado.ioloop
import tornado.web
import tornado.log
import json
import requests
import datetime

from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('weather', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get (self):
    self.set_header('Cache-Control',
     'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("index.html", {})

  def post (self):
    cityname = self.get_body_argument('cityname')
    url = "http://api.openweathermap.org/data/2.5/weather"
    querystring = {"q": cityname,"APIKEY":"2e32ce8e4192c1446ca78334f23e1ecb","units":"imperial"}
    headers = {
        'cache-control': "no-cache",
        'postman-token': "16ca84d0-4102-9b21-8f21-a9acd570d842"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    response = json.loads(response.text)
    # print(response)
    # response.sys.sunrise = datetime.datetime.utcfromtimestamp(response.sys.sunrise)
    # response.sys.sunset = datetime.datetime.utcfromtimestamp(response.sys.sunset)
#or you could do this for convenience (refer below)
    # clouds = response.text.weather[0].temp
    # temp = response.text.weather[0].temp
    # print(json.loads(response.text))
    self.render_template('results.html', {'response': response})

#or you could do this for convenience
#  self.render_template('results.html', {'clouds' : clouds, 'temp': temp })



    # render the weather data

class ResultsHandler(TemplateHandler):
    def get(self):
        self.render_template("results.html", {})


def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/", ResultsHandler),
    (r"/static/(.*)",
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)

if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8080')))
  tornado.ioloop.IOLoop.current().start()
