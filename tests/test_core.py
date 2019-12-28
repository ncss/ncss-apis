def test_root(client):
  res = client.get("/")
  assert res.status_code == 302
  assert "/docs" in res.location

def test_api_spec(client):
  res = client.get("/api/spec")
  assert res.status_code == 200
  data = res.get_json()
  assert 'info' in data
  assert 'version' in data['info']
