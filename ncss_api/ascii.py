from ascii_art import Bar
from art import text2art
from flask import request, abort, jsonify

from .app import app
from .utils import plain_textify

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
  return plain_textify(text2art(value, font=font))

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
  return plain_textify(b.render())


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
