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
