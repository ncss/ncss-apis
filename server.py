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

    return jsonify({'error': code, 'message': message})

@app.route('/emoji/<key>', methods=['GET', 'POST'])
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
  emojis = set(emojislib.search_by_key(key) + emojislib.search_by_name(key) + emojislib.search_by_cate(key))
  print(emojis)

  if emojis:
    return str(random.choice(list(emojis)))
  else:
    abort(404)

@app.route('/syllables/<word>', methods=['GET', 'POST'])
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

@app.route('/moonphase', methods=['GET', 'POST'])
def moon_phase_api():
  """
    Show the moon's phase for a given date
    ---
    tags:
      - moon phase 
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

@app.route('/convert/number', methods=['GET', 'POST'])
def numerals_api():
  """
    Convert numbers into different representations (e.g., 1, one, first)
    ---
    tags:
      - convert
      - number 
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

@app.route('/convert/unit', methods=['GET', 'POST'])
def units_api():
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


@app.route('/asciiart/text', methods=['GET', 'POST'])
def ascii_art_api():
  value = request.args.get('value', '')
  font = request.args.get('font')
  return text2art(value, font=font)

@app.route('/chart/bar', methods=['GET', 'POST'])
def chart_bar_api():
  data = {key: float(value) for key, value in request.args.items()}
  b = Bar(data)
  return b.render()

@app.route('/goldenhour', methods=['GET', 'POST'])
def goldenhour_api():
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

@app.route('/secret', methods=['GET', 'POST'])
def secret():
  random.seed(a='secret')
  secret = ''.join(random.sample(string.printable, 100))
  return secret

if __name__ == '__main__':
  app.run(debug=True)
