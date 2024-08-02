import client

def test_ping():
    assert client.ping() == "It works!"
