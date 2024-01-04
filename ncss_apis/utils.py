from flask import make_response

def plain_textify(string):
    """Convert a string to a UTF-8 encoded body with the text/plain
    mimetype."""
    resp = make_response(string)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp
