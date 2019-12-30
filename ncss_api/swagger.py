from flask import jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from .app import app

SWAGGER_URL = '/docs'
API_URL = '/api/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'NCSS APIs', 'deepLinking': True},
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/api/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'NCSS APIs'
    return jsonify(swag)
