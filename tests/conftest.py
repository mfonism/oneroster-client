import os

import pytest


@pytest.fixture(autouse=True)
def setup_environment():
    original_token_url = os.getenv("TOKEN_URL")
    original_base_url = os.getenv("BASE_URL")

    os.environ["TOKEN_URL"] = "https://test.com/token"
    os.environ["BASE_URL"] = "https://test.com/api"

    yield

    if original_token_url is not None:
        os.environ["TOKEN_URL"] = original_token_url
    else:
        del os.environ["TOKEN_URL"]

    if original_base_url is not None:
        os.environ["BASE_URL"] = original_base_url
    else:
        del os.environ["BASE_URL"]
