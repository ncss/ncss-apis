def test_invalid(client):
  res = client.get("/syllables/")
  assert res.status_code == 404

def test_count_syllables(client):
  assert_count(client, "dog", 1)
  assert_count(client, "hello", 2)
  assert_count(client, "fabulous", 3)

def assert_count(client, word, count):
  res = client.get(f"/syllables/{word}")
  assert res.status_code == 200
  data = res.data.decode("utf-8")
  assert data == str(count)
