from flask import Flask, request, jsonify

import syllables

app = Flask('ncss-apis')

@app.route('/syllables/<word>', methods=['GET', 'POST'])
def syllables_api(word=''):
  return str(syllables.estimate(word))

if __name__ == '__main__':
  app.run(debug=True)
