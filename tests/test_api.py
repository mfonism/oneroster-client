import api


def test_client():
    client = api.Client()

    assert client.token_url == "https://test.com/token"
    assert client.base_url == "https://test.com/api"
