from flask import Flask, request, abort, jsonify

import emojislib
import random

import syllables

from astral import Astral
from datetime import datetime

from num2words import num2words
from words2num import w2n as words2num

from art import text2art

from ascii_art import Bar

app = Flask('ncss-apis')

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
