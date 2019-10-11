from flask import Flask, request, jsonify

import syllables
from astral import Astral
from datetime import datetime

app = Flask('ncss-apis')

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

if __name__ == '__main__':
  app.run(debug=True)
