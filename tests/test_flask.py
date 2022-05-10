import pytest
import sys

sys.path.append("..")
from flask import url_for
import server
import json


@pytest.fixture()
def app():
    app = server.app
    app.testing = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_empty_request(client):
    data = {"recommend_on": json.dumps([]), "movie_exceptions": json.dumps([])}

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 200


def test_exceptions_request(client):
    data = {
        "recommend_on": json.dumps([]),
        "movie_exceptions": json.dumps(
            ["62740938459a7d03615407b7", "62740938459a7d03615407b7"]
        ),
    }

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 200


def test_movie_request(client):
    data = {
        "recommend_on": json.dumps(
            ["62740938459a7d03615407b7", "62740938459a7d03615407b7"]
        ),
        "movie_exceptions": json.dumps([]),
    }

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 200


def test_full_request(client):
    data = {
        "recommend_on": json.dumps(["62740938459a7d03615407b7"]),
        "movie_exceptions": json.dumps(["62740938459a7d03615407b7"]),
    }

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 200


def test_404_request(client):
    data = {
        "recommend_on": json.dumps(["62740938459a7d03615407b7"]),
        "movie_exceptions": json.dumps(["62740938459a7d03615407b7"]),
    }

    response = client.get("/", query_string=data)

    assert response.status_code == 404


def test_no_movie_request(client):
    data = {
        "recommend_on": json.dumps(["627409384d03615407b7"]),
        "movie_exceptions": json.dumps(["62740938459a7d03615407b7"]),
    }

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 404


def test_no_movie_exception_request(client):
    data = {
        "recommend_on": json.dumps(["62740938459a7d03615407b7"]),
        "movie_exceptions": json.dumps(["627459a7d03615407b7"]),
    }

    response = client.get("/get_recommendation", query_string=data)

    assert response.status_code == 200
