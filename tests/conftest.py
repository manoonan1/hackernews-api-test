import pytest

from src.client import HNClient


@pytest.fixture
def client():
    with HNClient() as c:
        yield c
