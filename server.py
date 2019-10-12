from flask import Flask, request, abort, jsonify
from werkzeug.exceptions import HTTPException

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

app = Flask('ncss-apis')

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
  emojis = set(emojislib.search_by_key(key) + emojislib.search_by_name(key) + emojislib.search_by_cate(key))
  print(emojis)

  if emojis:
    return str(random.choice(list(emojis)))
  else:
    abort(404)

@app.route('/syllables/<word>', methods=['GET', 'POST'])
def syllables_api(word=''):
  return str(syllables.estimate(word))

@app.route('/moonphase', methods=['GET', 'POST'])
def moon_phase_api():
  a = Astral()
  phase = a.moon_phase(datetime.now())

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

if __name__ == '__main__':
  app.run(debug=True)
