from astral import Astral
from flask import request, abort
from datetime import datetime

from .app import app
from .utils import plain_textify

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

  if not year:
    abort(400, 'No year parameter given')
  if not day:
    abort(400, 'No day parameter given')
  if not month:
    abort(400, 'No month parameter given')

  try:
    year = int(year)
  except:
    abort(400, 'Year is an invalid number')
  try:
    month = int(month)
  except:
    abort(400, 'Month is an invalid number')
  try:
    day = int(day)
  except:
    abort(400, 'Day is an invalid number')

  try:
    dt = datetime(year, month, day)
  except ValueError:
    abort(400, 'Invalid date')

  phase = a.moon_phase(dt)

  if phase < 3.5:
    phase_text = "New Moon"
  elif phase < 10.5:
    phase_text = "First Quarter"
  elif phase < 17.5:
    phase_text = "Full Moon"
  elif phase < 24.5:
    phase_text = "Last Quarter"
  else:
    phase_text = "New Moon"

  return plain_textify(phase_text)


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
    abort(404, "city not found in database")

  start = city_data.time_at_elevation(174)
  end = city_data.time_at_elevation(184)
  time = lambda dt: dt.strftime('%-I:%M %p')

  return plain_textify(f'Golden hour is {time(start)} - {time(end)} in {city}')
