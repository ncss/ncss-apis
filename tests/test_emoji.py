def test_emoji_not_found(client):
  res = client.get("/emoji/")
  assert res.status_code == 404

  res = client.get("/emoji/jkxcgtnuehibetqhdu")
  assert res.status_code == 404

def test_good_emoji(client):
  res = client.get("/emoji/dog")
  assert res.status_code == 200
  emoji = res.data.decode("utf-8")
  assert emoji in {'🐾', '🐩'}
