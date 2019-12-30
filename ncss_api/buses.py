import csv
from datetime import datetime

from flask import request, abort, jsonify

from .app import app

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
  data = request.get_json()

  if data is None:
    abort(400, "expecting json object in request body")

  stop_id = data.get("stop_id")
  if not stop_id:
    abort(400, "stop_id is required")

  stop = [stop for stop in stops if stop['stop_id'] == stop_id]
  if not stop:
    abort(404, 'Stop not found')
  else:
    stop = stop[0]

  parse_time = lambda t: datetime.strptime(t, "%H:%M:%S").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
  format_time = lambda dt: dt.strftime('%-I:%M %p')
  try:
    if 'time' in data:
      query_time = parse_time(data['time'])
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
