import random
import string

from flask import request, abort, jsonify

from .app import app
from .utils import plain_textify

@app.route('/secret', methods=['GET'])
def secret():
  '''
    Ssssh it's a secret
    ---
    tags:
      - secret
    responses:
      200:
        description: The secret response
        content:
          text/plain:
            schema:
              type: string
              example: I'm not revealing my secret!
  '''
  random.seed(a='secret')
  secret = ''.join(random.choices(string.ascii_letters+string.digits, k=100))
  return plain_textify(secret)
