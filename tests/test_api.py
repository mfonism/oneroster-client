import pytest
import requests
import requests_mock

import api


def test_client():
    client = api.Client("a-test-client-id", "a-test-client-secret")

    assert client.token_url == "https://test.com/token"
    assert client.base_url == "https://test.com/api"
    assert client.client_id == "a-test-client-id"
    assert client.client_secret == "a-test-client-secret"

    assert client.access_token == "a-test-access-token"


def test_get_headers(client_id, client_secret):
    client = api.Client(client_id, client_secret)
    headers = client.get_headers()

    assert headers == {
        "Authorization": "Bearer a-test-access-token",
        "Content-Type": "application/json",
    }


def test_fetch_data(client_id, client_secret):
    client = api.Client(client_id, client_secret)
    url = f"{client.base_url}/test-data"

    with requests_mock.Mocker() as m:
        m.get(url, json={"key": "value"})

        response = client.fetch_data(url)
        assert response == {"key": "value"}


def test_fetch_data_raises_for_status(client_id, client_secret):
    client = api.Client(client_id, client_secret)
    url = f"{client.base_url}/test-data"

    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)

        with pytest.raises(requests.exceptions.HTTPError):
            client.fetch_data(url)
