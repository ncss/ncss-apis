from flask import Flask, request, abort, jsonify

import emojislib
import random

import syllables

from astral import Astral
from datetime import datetime

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

@app.route('/chart/bar', methods=['GET', 'POST'])
def chart_bar_api():
  data = {key: float(value) for key, value in request.args.items()}
  b = Bar(data)
  return b.render()

if __name__ == '__main__':
  app.run(debug=True)
