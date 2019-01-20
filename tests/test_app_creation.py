import pytest
import json

def test_status_added_with_zip(app):
    rv = app.get('/api/v1/added/10247')
    assert rv.status_code == 200


def test_status_num_buildings_with_zip(app):
    rv = app.get('/api/v1/number_of_buildings/10247')
    assert rv.status_code == 200


def test_status_added(app):
    rv = app.get('/api/v1/added')
    assert rv.status_code == 200


def test_status_num_buildings(app):
    rv = app.get('/api/v1/number_of_buildings')
    assert rv.status_code == 200


def test_get_number_of_buildings(app):
    data = app.get('/api/v1/number_of_buildings')
    expected_response = json.dumps({
       10247: 4,
       10248: 3
    })
    assert data.json == expected_response


def test_get_number_of_buildings_by_zip_with_buildings(app):
    data = app.get('/api/v1/number_of_buildings/10247')
    expected_response = json.dumps({
       10247: 4,
    })
    assert data.json == expected_response


def test_get_number_of_buildings_by_zip_without_buildings(app):
    data = app.get('/api/v1/number_of_buildings/10345')
    expected_response = json.dumps({
    })
    assert data.json == expected_response


def test_get_number_added(app):
    data = app.get('/api/v1/added')
    expected_response = json.dumps({
        1960: 3,
        1961: 4
    })
    assert data.json == expected_response


def test_get_number_added_by_zip(app):
    data = app.get('/api/v1/added/10247')
    expected_response = json.dumps({
        1960: 2,
        1961: 2
    })
    assert data.json == expected_response

    data = app.get('/api/v1/added/10248')
    expected_response = json.dumps(
        {
            1960: 1,
            1961: 2
        }
    )
    assert data.json == expected_response


def test_get_number_added_by_zip_with_no_buildings(app):
    data = app.get('/api/v1/added/10345')
    expected_response = json.dumps({})
    assert data.json == expected_response
