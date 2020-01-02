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
  by_key = list(emojislib.by_key(key))
  by_name = [emojislib.by_name(key).char] if emojislib.by_name(key) else []
  search_by_name = list(emojislib.search_by_name(key))
  search_by_key = list(emojislib.search_by_key(key))
  search_by_category = list(emojislib.search_by_cate(key))
  emojis = set(by_key or by_name or search_by_name or search_by_key or search_by_category)

  if emojis:
    return plain_textify(str(random.choice(list(emojis))))
  else:
    abort(404)

