import pytest

from ncss_apis import app

@pytest.fixture
def client():
  client = app.test_client()
  yield client
