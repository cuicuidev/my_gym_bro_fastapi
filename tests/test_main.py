from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_get_set():
    pass