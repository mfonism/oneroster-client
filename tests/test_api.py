import api


def test_client():
    client = api.Client("a-test-client-id", "a-test-client-secret")

    assert client.token_url == "https://test.com/token"
    assert client.base_url == "https://test.com/api"
    assert client.client_id == "a-test-client-id"
    assert client.client_secret == "a-test-client-secret"

    assert client.access_token == "a-test-access-token"
