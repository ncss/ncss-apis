from ascii_art import Bar
from art import text2art
from flask import request, abort

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
  art = text2art(value, font=font).replace('\r\n', '\n')
  return plain_textify(art)

@app.route('/chart/bar', methods=['GET'])
def chart_bar_api():
  '''
    Render data as a bar chart using ASCII art. Any number of key/value pairs may be provided.
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
  try:
    data = {key: float(value) for key, value in request.args.items()}
  except ValueError:
    abort(400, "One or more values was not a valid integer")

  if not data:
    abort(400, "Must provide at least one key/value pair")

  b = Bar(data)
  return plain_textify(b.render())


@app.route('/woah', methods=['GET'])
def woah():
  '''
    Basic endpoint to catch "the woah"
    ---
    tags:
      - ASCII
    parameters:
      - in: query
        name: woah
        schema:
          type: string
          example: "catch the woah!"
        description: We just want to check if the woah key is present. Then we know that you've thrown the woah!
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
  woah = request.args.get('woah')

  if woah is None:
    abort(400, "No woah was thrown :(")
  else:
    return plain_textify(catch)
