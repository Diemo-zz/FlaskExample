import pytest
import json
from application import URI


def test_uri():
    text = "first"
    expected_text = '/api/v1/first'
    assert URI(text) == expected_text


def create_new_user():
    rv = app.get('/api/v1/users/1')
    assert rv.status_code == 200


