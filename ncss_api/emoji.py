import random

from flask import request, abort, jsonify
import emojislib

from .app import app
from .utils import plain_textify

@app.route('/emoji/<key>', methods=['GET'])
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
  emojis = set(emojislib.by_key(key) or emojislib.by_name(key) or emojislib.search_by_name(key) or emojislib.search_by_key(key) or emojislib.search_by_cate(key))

  if emojis:
    return plain_textify(str(random.choice(list(emojis))))
  else:
    abort(404)

