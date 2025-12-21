import time  # noqa F401

import pytest


def test_first():
    assert "hello" in "hello world"


@pytest.mark.second
def test_second():
    assert len("hello") == 5
