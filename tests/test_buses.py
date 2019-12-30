def test_example(client):
  """
  This tests the example on https://groklearning.com/learn/ncss-2020-web/json-http-requests/22/ | HTTP Requests with JSON
  """
  data = {
    'stop_id': '82',
    'time': '07:15:00'
  }

  res = client.post("/buses/hail", json=data)
  assert res.status_code == 200
  response_data = res.get_json()
  assert "message" in response_data
