from application import create_application
import pytest

def test_config():
    assert not create_application().testing
    assert create_application({'TESTING': True}).testing