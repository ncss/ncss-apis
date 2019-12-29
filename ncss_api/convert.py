from flask import request, abort
from num2words import num2words
from words2num import w2n as words2num
import pint

from .app import app
from .utils import plain_textify

units = pint.UnitRegistry()
units.define('tims = 1.5 * m = tims')

@app.route('/convert/number', methods=['GET'])
def numerals_api():
  """
    Convert numbers into different representations (e.g., 1, one, first)
    ---
    tags:
      - convert
    parameters:
      - in: query
        name: value
        required: true
        schema:
          type: string
          example: 11
        description: the value you would like to convert
      - in: query
        name: to
        type: string
        default: words
        example: words
        enum: ["words", "rank", "number"]
        description: the kind of value you would like to convert to
    responses:
      200:
        description: The converted value
        content:
          text/plain:
            schema:
              type: string
              example: eleven
  """
  value = request.args.get('value')
  to = request.args.get('to', 'words')

  if value:
    if to == 'words':
      return plain_textify(num2words(value, to='cardinal'))
    elif to =='rank':
      return plain_textify(num2words(value, to='ordinal'))
    elif to == 'number':
      return plain_textify(str(words2num(value)))
    else:
      abort(400, "unknown 'to' value")
  else:
    abort(400, "value to convert is required")

@app.route('/convert/unit', methods=['GET'])
def units_api():
  '''
    Convert a value from one unit to another
    ---
    tags:
      - convert
    parameters:
      - in: query
        name: quantity
        required: true
        schema:
          type: number
          example: 3.14
        description: the quantity you would like to convert
      - in: query
        name: unit
        required: true
        schema:
          type: string
          example: km
        description: the unit you would like to convert from
      - in: query
        name: to
        required: true
        schema:
          type: string
          example: m
        description: the unit you would like to convert to
    responses:
      200:
        description: The converted value
        content:
          text/plain:
            schema:
              type: string
              example: 3140 metres
  '''
  quantity = request.args.get('quantity')
  unit = request.args.get('unit')
  to = request.args.get('to')

  if quantity == None:
    abort(400, 'No quantity parameter given')
  if unit == None:
    abort(400, 'No unit parameter given')
  if to == None:
    abort(400, 'No to parameter given')

  try:
    unitless_quantity = units.parse_expression(quantity)
  except pint.errors.DefinitionSyntaxError:
    abort(400, f'Quantity {quantity!r} is invalid')
  try:
    from_unit = units.parse_expression(unit)
  except pint.errors.UndefinedUnitError:
    abort(404, f'Unit {unit!r} not found')
  try:
    to_unit = units.parse_expression(to)
  except pint.errors.UndefinedUnitError:
    abort(404, f'Unit {unit!r} not found')

  value = unitless_quantity * from_unit

  try:
    to_value = value.to(to_unit)
  except pint.errors.DimensionalityError:
    abort(400, f'Cannot convert from {unit} to {to}')

  return plain_textify(f'{to_value:P}')

