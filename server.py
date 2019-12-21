from flask import Flask, request, abort, jsonify, redirect
from werkzeug.exceptions import HTTPException

from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

import emojislib
import random

import syllables

from astral import Astral
from datetime import datetime

from num2words import num2words
from words2num import w2n as words2num

import pint

from art import text2art

from ascii_art import Bar

import string

import csv

app = Flask('ncss-apis')

SWAGGER_URL = '/docs' 
API_URL = '/api/spec' 
swaggerui_blueprint = get_swaggerui_blueprint( 
    SWAGGER_URL, 
    API_URL, 
    config={'app_name': 'NCSS APIs', 'deepLinking': True}, 
) 
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) 
 
 
@app.route("/api/spec") 
def spec(): 
    swag = swagger(app) 
    swag['info']['version'] = '1.0' 
    swag['info']['title'] = 'NCSS APIs' 
    return jsonify(swag)


@app.route('/')
def hello():
    return redirect("/docs", code=302)

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        code = e.code
        message = e.description
    else:
      code = 500
      message = f'There was an internal server error'
      app.logger.error(e)

    return jsonify({'error': code, 'message': message}), code

@app.route('/emoji/<key>', methods=['GET'])
def emoji_api(key=''):
  """
    Fetch an Emoji
    ---
    tags:
      - emoji 
    parameters:
      - in: path
        name: key 
        required: true
        schema:
          type: string
          example: dog
        description: the emoji you would like to search for
    responses:
      200:
        description: A random emoji matching your search
        content:
          text/plain:
            schema:
              type: string
              example: 🐩
  """
  emojis = set(emojislib.by_key(key) or emojislib.by_name(key) or emojislib.search_by_name(key) or emojislib.search_by_key(key) or emojislib.search_by_cate(key))

  if emojis:
    return str(random.choice(list(emojis)))
  else:
    abort(404)

@app.route('/syllables/<word>', methods=['GET'])
def syllables_api(word=''):
  """
    Count the syllables in a word 
    ---
    tags:
      - syllables 
    parameters:
      - in: path
        name: word 
        required: true
        schema:
          type: string
          example: hello
        description: the word you would like to count the syllables of 
    responses:
      200:
        description: The number of syllables 
        content:
          text/plain:
            schema:
              type: string
              example: 2
  """
  return str(syllables.estimate(word))

@app.route('/moonphase', methods=['GET'])
def moon_phase_api():
  """
    Show the moon's phase for a given date
    ---
    tags:
      - astronomy 
    parameters:
      - in: query
        name: year 
        required: true
        schema:
          type: integer 
          example: 2019
        description: the year you would like the moon phase for
      - in: query
        name: month 
        required: true
        schema:
          type: integer 
          example: 1
        description: the month you would like the moon phase for
      - in: query
        name: day 
        required: true
        schema:
          type: integer 
          example: 13
        description: the day of the month you would like the moon phase for
    responses:
      200:
        description: The moon phase 
        content:
          text/plain:
            schema:
              type: string
              example: Full Moon
  """
  a = Astral()
  year = request.args.get('year')
  month = request.args.get('month')
  day = request.args.get('day')

  if year == None:
    abort(400, 'No year parameter given')
  else:
    year = int(year)
  if month == None:
    abort(400, 'No month parameter given')
  else:
    month = int(month)
  if day == None:
    abort(400, 'No day parameter given')
  else:
    day = int(day)

  phase = a.moon_phase(datetime(year, month, day))

  if phase < 3.5:
    return "New Moon"
  elif phase < 10.5:
    return "First Quarter"
  elif phase < 17.5:
    return "Full Moon"
  elif phase < 24.5:
    return "Last Quarter"
  else:
    return "New Moon"

@app.route('/convert/number', methods=['GET'])
def numerals_api():
  """
    Convert numbers into different representations (e.g., 1, one, first)
    ---
    tags:
      - convert
    parameters:
      - in: query
        name: value 
        required: true
        schema:
          type: string 
          example: 11
        description: the value you would like to convert
      - in: query
        name: to
        required: true
        schema:
          type: string 
          example: words
          enum: [words, rank, number]
        description: the kind of value (words | rank | number) you would like to convert to
    responses:
      200:
        description: The converted value 
        content:
          text/plain:
            schema:
              type: string
              example: eleven
  """
  value = request.args.get('value')
  to = request.args.get('to', 'cardinal')

  if value:
    if to == 'cardinal' or to == 'words':
      return num2words(value, to='cardinal')
    elif to == 'ordinal' or to =='rank':
      return num2words(value, to='ordinal')
    elif to == 'numerals' or to == 'number':
      return str(words2num(value))
    else:
      abort(400)
  else:
    abort(400)

units = pint.UnitRegistry()
units.define('tims = 1.5 * m = tims')

@app.route('/convert/unit', methods=['GET'])
def units_api():
  '''
    Convert a value from one unit to another
    ---
    tags:
      - convert
    parameters:
      - in: query
        name: quantity
        required: true
        schema:
          type: number
          example: 3.14
        description: the quantity you would like to convert
      - in: query
        name: unit
        required: true
        schema:
          type: string
          example: km
        description: the unit you would like to convert from
      - in: query
        name: to
        required: true
        schema:
          type: string
          example: m
        description: the unit you would like to convert to
    responses:
      200:
        description: The converted value 
        content:
          text/plain:
            schema:
              type: string
              example: 3140 metres
  '''
  quantity = request.args.get('quantity')
  unit = request.args.get('unit')
  to = request.args.get('to')

  if quantity == None:
    abort(400, 'No quantity parameter given')
  if unit == None:
    abort(400, 'No unit parameter given')
  if to == None:
    abort(400, 'No to parameter given')

  try:
    unitless_quantity = units.parse_expression(quantity)
  except pint.errors.DefinitionSyntaxError:
    abort(400, f'Quantity {quantity!r} is invalid')
  try:
    from_unit = units.parse_expression(unit)
  except pint.errors.UndefinedUnitError:
    abort(404, f'Unit {unit!r} not found')
  try:
    to_unit = units.parse_expression(to)
  except pint.errors.UndefinedUnitError:
    abort(404, f'Unit {unit!r} not found')

  value = unitless_quantity * from_unit

  try:
    to_value = value.to(to_unit)
  except pint.errors.DimensionalityError:
    abort(400, f'Cannot convert from {unit} to {to}')

  return f'{to_value:P}'


@app.route('/asciiart/text', methods=['GET'])
def ascii_art_api():
  '''
    Render a string using ASCII art
    ---
    tags:
      - ASCII
    parameters:
      - in: query
        name: string 
        required: true
        schema:
          type: string
          example: Shelley
        description: the string you would like rendered using ASCII art 
      - in: query
        name: font
        required: true
        schema:
          type: string
          enum: ['1943', '3d_diagonal', 'epic', 'graffiti', 'isometric1', 'sub-zero', 'nscript', 'nancyj', 'black_square', 'upside_down']
          example: 3d
        description: the [font](https://github.com/sepandhaghighi/art/blob/master/FontList.ipynb) used to render the ASCII text in
    responses:
      200:
        description: The converted value 
        content:
          text/plain:
            schema:
              type: string
              example: 3140 metres
  '''
  value = request.args.get('string', '')
  font = request.args.get('font')
  return text2art(value, font=font)

@app.route('/chart/bar', methods=['GET'])
def chart_bar_api():
  '''
    Render data as a bar chart using ASCII art
    ---
    tags:
      - ASCII 
    parameters:
      - in: query
        name: item1
        schema:
          type: integer
          example: 12
        description: an example of a key/value pair
      - in: query
        name: item2
        schema:
          type: integer
          example: 23
        description: an example of a key/value pair
      - in: query
        name: item3
        schema:
          type: integer
          example: 1
        description: an example of a key/value pair
    responses:
      200:
        description: The bar chart
        content:
          text/plain:
            schema:
              type: string
              example: item1 | ###############################                              | 12.0
  '''
  data = {key: float(value) for key, value in request.args.items()}
  b = Bar(data)
  return b.render()

@app.route('/goldenhour', methods=['GET'])
def goldenhour_api():
  '''
    Find out the time of today's 'golden hour' for a given city
    ---
    tags:
      - astronomy
    parameters:
      - in: query
        name: city
        schema:
          type: string 
          example: Sydney
          default: Sydney
        description: the city you want to know the time of golden hour in
    responses:
      200:
        description: A description of the time of golden hour 
        content:
          text/plain:
            schema:
              type: string
              example: Golden hour is 7:27pm - 8:22pm in Sydney'
  '''
  city = request.args.get('city', 'Sydney')

  a = Astral()
  a.solar_depression = 'civil'
  try:
    city_data = a[city]
  except KeyError:
    abort(404)

  start = city_data.time_at_elevation(174)
  end = city_data.time_at_elevation(184)
  time = lambda dt: dt.strftime('%-I:%M %p')

  return f'Golden hour is {time(start)} - {time(end)} in {city}'

@app.route('/secret', methods=['GET'])
def secret():
  '''
    Ssssh it's a secret
    ---
    tags:
      - secret
    responses:
      200:
        description: The secret response 
        content:
          text/plain:
            schema:
              type: string
              example: I'm not revealing my secret!
  '''
  random.seed(a='secret')
  secret = ''.join(random.sample(string.printable, 100))
  return secret

stops = list(csv.DictReader(open('data/buses/stops.txt', encoding="utf-8-sig")))
stop_times = list(csv.DictReader(open('data/buses/stop_times.txt', encoding="utf-8-sig")))
routes = list(csv.DictReader(open('data/buses/routes.txt', encoding="utf-8-sig")))

@app.route('/buses/stops', methods=['GET'])
def bus_stops():
  '''
    Locations of bus stops
    ---
    tags:
      - buses
    responses:
      200:
        description: An array of JSON objects each describing a single stop
        schema:
          id: Stops
          type: array
          items:
            type: object
            properties:
              stop_id:
                type: string
                example: '82'
                description: the unique ID for the bus stop
              stop_name:
                type: string
                example: 'Power Street'
                description: the name of the stop
              stop_lat:
                type: string
                example: '-23.669039'
                description: the latitude of the stop
              stop_lng:
                type: string
                example: '133.868417'
                description: the longitude of the stop
              zone_id:
                type: string
                example: '2'
                description: the zone ID for the bus stop
  '''
  return jsonify(stops)

@app.route('/buses/stop_times', methods=['GET'])
def bus_stop_times():
  '''
    Times buses stop
    ---
    tags:
      - buses
    responses:
      200:
        description: An array of JSON objects each describing the buses' stopping times
        schema:
          id: StopTimes
          type: array
          items:
            type: object
            properties:
              stop_id:
                type: string
                example: '82'
                description: the ID for the bus stop
              trip_id:
                type: string
                example: '1848'
                description: the ID of the bus trip
              stop_sequence:
                type: string
                example: '2'
                description: the number stop this is in a particular trip
              arrival_time:
                type: string
                example: '7:04:00'
                description: the time the bus arrives
  '''
  return jsonify(stop_times)

@app.route('/buses/routes', methods=['GET'])
def bus_routes():
  '''
    Routes for buses
    ---
    tags:
      - buses
    responses:
      200:
        description: An array of JSON objects each describing each route 
        schema:
          id: Routes
          type: array
          items:
            type: object
            properties:
              route_id:
                type: string
                example: '1600'
                description: the unique ID for the bus route
              route_long_name:
                type: string
                example: 'The Gap and Ross'
                description: the name for the bus route
              route_short_name:
                type: string
                example: '301'
                description: the route number/ID for the bus route
              route_color:
                type: string
                example: '004C5B'
                description: the canonical colour used for the route in maps and diagrams
  '''
  return jsonify(routes)

@app.route('/buses/hail', methods=['POST'])
def bus_hail():
  '''
    Hail a bus at a given stop
    ---
    tags:
      - buses
    consumes:
      - application/json
    parameters:
      - in: body
        schema:
          id: Hail
          type: object
          properties:
            stop_id:
              required: True
              type: string
              example: '82'
              description: the id of the stop where you would like to hail the bus
            time:
              type: string
              example: '15:20:00'
              description: the time (24 hour time) you want to hail the bus
    responses:
      200:
        description: A JSON object confirming your hail
        content:
          text/json:
            schema:
              properties:
                message:
                  type: string
                  example: 'Hailing the bus at Power Street at 4:18 pm'
                  description: A message describing the result of your request
                stop:
                  id: Stop
                  type: object
                  description: An object describing the stop
                stop_times:
                  type: array
                  description: An list of objects describing the stop times
  '''
  try:
    data = request.get_json()
  except:
    data = request.form
  stop_id = data['stop_id']
  stop = [stop for stop in stops if stop['stop_id'] == stop_id]

  if not stop:
    abort(404, 'Stop not found')
  else:
    stop = stop[0]

  parse_time = lambda t: datetime.strptime(t, "%H:%M:%S").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
  format_time = lambda dt: dt.strftime('%-I:%M %p')
  try:
    if 'time' in request.form:
      query_time = parse_time(request.form['time'])
    else:
      query_time = datetime.now()
  except:
    abort(400, 'Time was not in the correct format')

  hail_stop_times = [stop_time for stop_time in stop_times if stop_time['stop_id'] == stop_id and parse_time(stop_time['arrival_time']) > query_time][:5]

  if hail_stop_times:
    hail = {
      'message': f'You can catch the bus at {stop["stop_name"]} from {format_time(parse_time(hail_stop_times[0]["arrival_time"]))}',
      'stop': stop,
      'stop_times': hail_stop_times,
    }
  else:
    hail = {
      'message': f'No buses will be stopping at {stop["stop_name"]}',
      'stop': stop,
      'stop_times': [],
    }

  print(hail)

  return jsonify(hail)

@app.route('/woah', methods=['GET'])
def woah():
  '''
    Basic endpoint to catch/throw "the woah"
    ---
    tags:
      - ASCII
    responses:
      200:
        description: A JSON object of us catching the woah
        content:
          text/json:
            schema:
              properties:
                message:
                  type: string
                  example: '        😲
                                  ✊|
                                    |✊
                                   / \\
                                  /    \\'
                  description: Caught the woah!
    
  '''
  catch = '''
        😲
       ✊|
         |✊
        / \\
      /    \\
  '''
  # udpated args syntax for GET request
  value = request.args.get('value')

  if value is None:
    abort(400, "No value field provided")
  elif "catch" in value: 
    return jsonify(catch)
  else:
    abort(400, "How can I catch if you didnt throw?")
    
if __name__ == '__main__':
  app.run(debug=True)
