import pytest

from ncss_api import app

@pytest.fixture
def client():
  client = app.test_client()
  yield client
