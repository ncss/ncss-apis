from flask import request, abort, jsonify

import syllables

import string

from .app import app
from .utils import plain_textify

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
  return plain_textify(str(syllables.estimate(word)))

