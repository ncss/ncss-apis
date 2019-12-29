def test_invalid(client):
  res = client.get("/woah")
  assert res.status_code == 400

  res = client.get("/woah", query_string={'value': 'invalid'})
  assert res.status_code == 400

def test_ok(client):
  res = client.get("/woah", query_string={'value': 'catch'})
  assert res.status_code == 200
  data = res.data.decode("utf-8")
  assert "😲" in data
