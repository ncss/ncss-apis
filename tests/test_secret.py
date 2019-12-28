def test_secret(client):
  res = client.get("/secret")
  assert res.status_code == 200
  assert res.data.startswith(b'{0g@')
