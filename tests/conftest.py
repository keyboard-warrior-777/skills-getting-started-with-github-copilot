import os
import sys
import copy
import pytest
from fastapi.testclient import TestClient

# Make the src directory importable for tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from app import app, activities


@pytest.fixture
def client():
    """Fixture that provides a TestClient and restores global state after each test."""
    original = copy.deepcopy(activities)
    with TestClient(app) as test_client:
        yield test_client
    # Restore global state after each test
    activities.clear()
    activities.update(original)
