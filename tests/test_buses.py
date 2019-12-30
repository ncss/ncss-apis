def test_example(client):
    """
    This tests the example on https://groklearning.com/learn/ncss-2020-web/json-http-requests/22/ | HTTP Requests with JSON
    """
    data = {"stop_id": "82", "time": "07:15:00"}

    res = client.post("/buses/hail", json=data)
    assert res.status_code == 200
    response_data = res.get_json()
    assert "message" in response_data
    assert len(response_data["stop_times"]) > 0


def test_hail_bus_types(client):

    # should error if stop id not provided
    data = {"stop_id": "", "time": "07:15:00"}
    res = client.post("/buses/hail", json=data)
    assert res.status_code == 400

    # should 404 if stop id not found
    data = {"stop_id": "garbage", "time": "07:15:00"}
    res = client.post("/buses/hail", json=data)
    assert res.status_code == 404

    # should 400 on garbage in body
    data = {"stop_id": "82", "time": "07:15:00"}
    res = client.post("/buses/hail", data=data)
    assert res.status_code == 400

    # should 400 on garbage time
    data = {"stop_id": "120", "time": "garbage"}
    res = client.post("/buses/hail", json=data)
    assert res.status_code == 400
    data = res.get_json()
    assert "Time" in data["message"]

    # check that no stop times for this combination
    data = {
        "stop_id": "120",
        "time": "23:04:50",
    }
    res = client.post("/buses/hail", json=data)
    assert res.status_code == 200
    data = res.get_json()
    assert data["stop_times"] == []

    # default to current time for stops
    data = {
        "stop_id": "120",
    }
    res = client.post("/buses/hail", json=data)
    assert res.status_code == 200
    data = res.get_json()
    assert "stop" in data
    assert isinstance(data, dict)


def test_basic_get_methods(client):
    res = client.get("/buses/stops")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) > 0
    assert "stop_id" in data[0]
    assert "stop_name" in data[0]

    res = client.get("/buses/stop_times")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) > 0
    assert "trip_id" in data[0]
    assert "departure_time" in data[0]

    res = client.get("/buses/routes")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) > 0
    assert "route_id" in data[0]
    assert "route_desc" in data[0]
