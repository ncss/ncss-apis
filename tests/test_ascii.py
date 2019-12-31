def test_woah_invalid(client):
    res = client.get("/woah")
    assert res.status_code == 400

    res = client.get("/woah", query_string={"invalid_key": "invalid_value"})
    assert res.status_code == 400


def test_woah_ok(client):
    res = client.get("/woah", query_string={"woah": "catch the woah!"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert "😲" in data


def test_asciiart_text(client):
    # empty text is ok, but empty string in response
    res = client.get("/asciiart/text", query_string={"font": "graffiti"})
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    assert data == ""

    # now something valid
    res = client.get(
        "/asciiart/text", query_string={"string": "hello", "font": "graffiti"}
    )
    assert res.status_code == 200
    data = res.data.decode("utf-8")
    # note: trailing whitespace is required
    assert (
        data
        == r""".__             .__   .__           
|  |__    ____  |  |  |  |    ____  
|  |  \ _/ __ \ |  |  |  |   /  _ \ 
|   Y  \\  ___/ |  |__|  |__(  <_> )
|___|  / \___  >|____/|____/ \____/ 
     \/      \/                     
"""
    )


def test_barchart_invalid_input(client):
    # should not be allowed to give non-float values to query params
    res = client.get("/chart/bar", query_string={"one": "abc"})
    assert res.status_code == 400

    # should not be allowed to give no query params
    res = client.get("/chart/bar")
    assert res.status_code == 400


def test_barchart_valid(client):

    # this should work fine
    res = client.get("/chart/bar", query_string={"one": 1, "two": 2.5})
    data = res.data.decode("utf-8")
    assert (
        data
        == r"""
one | ########################                                     | 1.0
two | ############################################################ | 2.5
"""
    )
