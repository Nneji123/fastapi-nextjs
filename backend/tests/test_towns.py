import os
import sys
import time  # Import the time module
import warnings

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

# Get the current directory (where the test_towns.py file is located)
current_dir = os.path.dirname(os.path.realpath(__file__))

# Append the parent directory (project root) to the Python path
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from api.app import create_app  # Replace with your actual FastAPI app file
from api.config import test_settings

# Now you should be able to import your modules using absolute paths
from api.public.towns.models import *  # Replace with your Town model


@pytest.fixture(scope="module")
def test_app(settings=test_settings):
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    # Create a session per test module
    app = create_app(settings)
    with Session(engine) as session:
        yield TestClient(app), session


def test_create_town(test_app):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    client, session = test_app

    # Generate a unique name using a timestamp
    town_name = f"Town_{int(time.time())}"

    town_data = {"name": town_name, "population": 10000, "country": "Country A"}

    # Use the session from the fixture to interact with the database
    created_town = Town(**town_data)
    session.add(created_town)
    session.commit()

    response = client.post("/towns/", json=town_data)
    print(response.text)
    assert response.status_code == 200

    fetched_town = response.json()
    assert fetched_town["status"] == "success"  # Verify the overall status
    assert (
        fetched_town["msg"] == "Town created successfully"
    )  # Verify the success message
    assert fetched_town["data"]["name"] == town_name


def test_get_single_town(test_app):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    client, session = test_app
    town_name = f"Town_{int(time.time())}s"

    town_data = {"name": town_name, "population": 10000, "country": "Country A"}

    # Use the session from the fixture to interact with the database
    created_town = Town(**town_data)
    session.add(created_town)
    session.commit()

    # Assuming town with ID=1 exists in the database
    response = client.get(f"/towns/{created_town.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), TownReadWithPeople) == False


def test_get_all_towns(test_app):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    client, _ = test_app

    response = client.get("/towns/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for town in response.json():
        assert isinstance(town, TownRead) == False


def test_update_existing_town(test_app):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    client, _ = test_app

    # Assuming town with ID=1 exists in the database
    town_update_data = {
        "name": "Updated Town Name",
        "population": 15000,
        "country": "Updated Country",
    }
    response = client.put("/towns/1", json=town_update_data)
    assert response.status_code == 200
    assert isinstance(response.json(), TownRead) == False


def test_delete_existing_town(test_app):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    client, _ = test_app

    # Assuming town with ID=1 exists in the database
    response = client.delete("/towns/1")
    assert response.status_code == 200
