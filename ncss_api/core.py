from flask import jsonify, redirect
from werkzeug.exceptions import HTTPException

from .app import app

@app.route('/')
def hello():
    return redirect("/docs", code=302)

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        code = e.code
        message = e.description
    else:
      code = 500
      message = f'There was an internal server error'
      app.logger.error(e)

    return jsonify({'error': code, 'message': message}), code

