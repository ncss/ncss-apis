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
  agent = request.headers.get('User-Agent')
  # Probably a browser
  if 'Mozilla' in agent:
    return plain_textify('No peeking! Use the requests library!')
  else:
    random.seed(a='secret')
    secret = ''.join(random.choices(string.ascii_letters+string.digits, k=100))
    return plain_textify(secret)
