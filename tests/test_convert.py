import pytest


def test_convert_number(client):
    # 'value' query param is required
    res = client.get("/convert/number")
    assert res.status_code == 400

    # this should work (defaults to converting to words
    res = client.get("/convert/number", query_string={"value": 10})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "ten"

    # should have same result
    res = client.get("/convert/number", query_string={"value": 10, "to": "words"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "ten"

    # convert to ordinal
    res = client.get("/convert/number", query_string={"value": 10, "to": "rank"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "tenth"

    # convert from cardinal word to number
    res = client.get("/convert/number", query_string={"value": "eleven", "to": "number"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "11"

    # try converting to unsupported target (should fail)
    res = client.get("/convert/number", query_string={"value": 10, "to": "klingon"})
    assert res.status_code == 400

    # try converting an unexpected number (it should work)
    res = client.get("/convert/number", query_string={"value": -10.4, "to": "words"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "minus ten point four"


@pytest.mark.skip(reason="not implemented yet; 500 errors")
def test_convert_number_invalid_input(client):
    # converting a number back to a number is invalid
    res = client.get("/convert/number", query_string={"value": 10, "to": "number"})
    assert res.status_code == 400

    # convert from word to ordinal/cardinal word should fail
    res = client.get("/convert/number", query_string={"value": "eleven", "to": "rank"})
    assert res.status_code == 400
    res = client.get("/convert/number", query_string={"value": "eleven", "to": "words"})
    assert res.status_code == 400

    # try converting not a number (should fail)
    res = client.get("/convert/number", query_string={"value": "bla", "to": "words"})
    assert res.status_code == 400

    # try converting not a word number (should fail)
    res = client.get("/convert/number", query_string={"value": "bla", "to": "number"})
    assert res.status_code == 400

def test_convert_units(client):
    # test the original example in the api docs
    query = {
        "quantity": "3.14",
        "unit": "km",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == "3140.0 meter"

    # all params are required, so should fail with client error if any are missing/empty
    query = {
        "quantity": "",
        "unit": "km",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400
    assert "quantity" in res.get_json()["message"].lower()

    query = {
        "quantity": "3.14",
        "unit": "",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400
    assert "unit" in res.get_json()["message"].lower()

    query = {
        "quantity": "3.14",
        "unit": "km",
        "to": "",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400
    assert "to" in res.get_json()["message"].lower()
    assert "unit" not in res.get_json()["message"].lower()

    # now test garbage quantities
    query = {
        "quantity": "yesterday",
        "unit": "km",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400

    query = {
        "quantity": "3.14ft",
        "unit": "km",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400

    # and garbage units (not found status, because the unit might be real, but
    # we couldn't find a definition for it)
    query = {
        "quantity": "3.14",
        "unit": "clearlynotaunit",
        "to": "m",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 404

    query = {
        "quantity": "3.14",
        "unit": "km",
        "to": "clearlynotaunit",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 404

    # now try to convert between units that don't make sense
    query = {
        "quantity": "3.14",
        "unit": "km",
        "to": "m^3",
    }
    res = client.get("/convert/unit", query_string=query)
    assert res.status_code == 400
    data = res.get_json()
    assert "cannot" in data["message"].lower()
