
from flask import redirect

from .app import app

@app.route('/sandwich/<key>', methods=['GET'])
def sandwich_api(key=''):
  """
    Return information on whether something is a sandwich.
    ---
    tags:
      - sandwich
    parameters:
      - in: path
        name: thing
        required: true
        schema:
          type: string
          example: lasagna
        description: the thing you would like to understand better, deep within yourself
    responses:
      200:
        description: A JSON object containing critical sandwich discourse. Absolutely essential to NCSS.
        content:
          text/json:
            schema:
              properties:
                message:
                  type: string
                  example: '{ "thing": "lasagna", "is_a": "sandwich", "confidence": 16, "finger_guns": true, "consider_also": [ "baguette" ] }'
                  description: critical information on your quest to understand why you want to be right about this so desperately.

  """

  # It's important to follow the protocol.
  return redirect("https://ncss-sandwich-api.appspot.com/" + key, 418)

