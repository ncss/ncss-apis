def test_goldenhour(client):
    # defaults to checking goldenhour for sydney
    res = client.get("/goldenhour")
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert "Sydney" in data
    assert "Golden hour is" in data

    # should be ok getting the hour for another city
    res = client.get("/goldenhour", query_string={"city": "Adelaide"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert "Adelaide" in data
    assert "Golden hour is" in data

    # check for standard not found response on garbage input
    res = client.get("/goldenhour", query_string={"city": "Hobbiton"})
    assert res.status_code == 404


def test_moonphase(client):
    # defaults to invalid
    res = client.get("/moonphase")
    assert res.status_code == 400

    # try something valid
    query = {
        "year": 2000,
        "month": 1,
        "day": 1,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "Last Quarter"

    # should still work
    query = {
        "year": 2019,
        "month": 12,
        "day": 29,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "New Moon"

    # test for the other implemented phases too
    query = {
        "year": 2019,
        "month": 12,
        "day": 25,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "New Moon"
    query = {
        "year": 2019,
        "month": 12,
        "day": 12,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "Full Moon"
    query = {
        "year": 2019,
        "month": 12,
        "day": 4,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "First Quarter"

def test_moonphase_invalid_input(client):
    # no month given
    query = {
        "year": 2000,
        "day": 29,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400
    data = res.data.decode("utf-8")
    assert "month" in data

    # no day given
    query = {
        "year": 2000,
        "month": 4,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400
    data = res.data.decode("utf-8")
    assert "day" in data


def test_moonphase_invalid_input2(client):
    # invalid year
    query = {
        "year": -45,
        "month": 4,
        "day": 1,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400
    query = {
        "year": "bla",
        "month": 4,
        "day": 1,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400

    # invalid month
    query = {
        "year": 2000,
        "month": 0,
        "day": 2,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400

    # not an integer
    query = {
        "year": 2000,
        "month": 4,
        "day": "yesterday",
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400

    # not an integer
    query = {
        "year": 2000,
        "month": 4.5,
        "day": 4,
    }
    res = client.get("/moonphase", query_string=query)
    assert res.status_code == 400
