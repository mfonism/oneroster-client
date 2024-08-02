import client


def test_ping():
    assert client.ping() == "It works!"


def test_pong():
    # this test will fail if you don't have an environment variable named
    # PONG, whose value is 'Really, it works!'
    # an easy way to do this is to create a .env file at the root of
    # the project, with the following content:
    # PONG="Really, it works!"
    assert client.pong() == "Really, it works!"
