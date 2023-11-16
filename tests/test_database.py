from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from core.database import Base, get_db, Set
import auth
import sets
from datetime import datetime, timedelta

from main import app

# <DATABASE MOCK SETUP>
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread" : False,
    },
    poolclass=StaticPool,
)

Base.metadata.create_all(bind=engine) # Create all tables

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine) # Create session object

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    except:
        db.close()

app.dependency_overrides[get_db] = override_get_db # Override the postgresql production database session with the mock sqlite database session
# </DATABASE MOCK SETUP>

# <CLIENT SETUP>
client = TestClient(app) # Client to make http requests to the api endpoints
# </CLIENT SETUP>

# <DATABASE TEST DATA SETUP>
def create_set_data(user_id: int):
    session = TestingSessionLocal()

    user_existing_set_schema = sets.schemas.Set(
        unix_timestamp_ms=datetime.now().timestamp(),

        weight_kg=50.0,
        n_repetitions=8,
        rir=2,
        duration_ms=40000.0,
        tir_ms=2000.0,

        exercise_id=1,

        previous_set_id=None,
        next_set_id=None,
    )

    user_existing_set = Set(**user_existing_set_schema.model_dump(), user_id=user_id, active=True)

    session.add_all([user_existing_set])
    session.commit()

    session.close()

def clean_set_data(user_id):
    session = TestingSessionLocal()

    # Retrieve and delete test data associated with the provided user_id
    sets_to_delete = session.query(Set).filter_by(user_id=user_id).all()

    for set_data in sets_to_delete:
        session.delete(set_data)

    session.commit()
    session.close()

def create_user_data():
    pass

def clean_user_data():
    pass

def create_exercise_data():
    pass

def clean_exercise_data():
    pass

def create_exercise_type_data():
    pass

def clean_exercise_type_data():
    pass

@pytest.fixture
def setup_mock_data():
    create_set_data(user_id=1)  # Create mock data before the test
    create_set_data(user_id=2)  # Create mock data before the test
    yield  # Continue with the test
    clean_set_data(user_id=1)
    clean_set_data(user_id=2)
# </DATABASE TEST DATA SETUP>

##################################################################################################### SET TABLE

############## GET
def test_get_set_authenticated_valid_set(setup_mock_data):
    # <SETUP>
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwidXNlcl9pZCI6MSwiZXhwIjoxNzE2MjM5MDIyfQ.gSo7AcCm387HUmu5lebK4li9ZWL7n04BPYfQQ1hiR30"
    users_existing_set_id = 1
    # <SETUP>

    response = client.get(
        f"/sets/get/{users_existing_set_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"Status code should be 200 for an existing set. Result: {response.status_code=}"
    assert response.json(), f"The response should contain a JSON body for an existing set. Result: {response.json()=}"

def test_get_set_authenticated_set_does_not_exist(setup_mock_data):
    # <SETUP>
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwidXNlcl9pZCI6MSwiZXhwIjoxNzE2MjM5MDIyfQ.gSo7AcCm387HUmu5lebK4li9ZWL7n04BPYfQQ1hiR30"
    non_existing_set_id = 3
    # <SETUP>

    response = client.get(
        f"/sets/get/{non_existing_set_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, f"Status code should be 404 for a non-existing set. Result: {response.status_code=}"

def test_get_set_authenticated_set_belongs_to_another_user(setup_mock_data):
    # <SETUP>
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwidXNlcl9pZCI6MSwiZXhwIjoxNzE2MjM5MDIyfQ.gSo7AcCm387HUmu5lebK4li9ZWL7n04BPYfQQ1hiR30"
    another_users_existing_set_id = 2
    # <SETUP>

    response = client.get(
        f"/sets/get/{another_users_existing_set_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403, f"Status code should be 403 if the set belongs to another user. Result: {response.status_code=}"

def test_get_set_not_authenticated(setup_mock_data):
    response = client.get("sets/get/{existing_id}")
    assert response.status_code == 401, f"Status code should be 401 for unauthenticated requests. Result: {response.status_code=}"


############## POST
def test_post_set_authenticated(setup_mock_data):
    pass

def test_post_set_not_authenticated(setup_mock_data):
    pass

############## PUT
def test_put_set_authenticated_valid_set(setup_mock_data):
    pass

def test_put_set_authenticated_set_does_not_exist(setup_mock_data):
    pass

def test_put_set_authenticated_set_belongs_to_another_user(setup_mock_data):
    pass

def test_put_set_not_authenticated(setup_mock_data):
    pass


############## DELETE
def test_delete_set_authenticated_valid_set(setup_mock_data):
    pass

def test_delete_set_authenticated_set_does_not_exist(setup_mock_data):
    pass

def test_delete_set_authenticated_set_belongs_to_another_user(setup_mock_data):
    pass

def test_delete_set_not_authenticated(setup_mock_data):
    pass


############## ACTIVATE
def test_activate_set_authenticated_valid_set(setup_mock_data):
    pass

def test_activate_set_authenticated_set_does_not_exist(setup_mock_data):
    pass

def test_activate_set_authenticated_set_belongs_to_another_user(setup_mock_data):
    pass

def test_activate_set_not_authenticated(setup_mock_data):
    pass

############## HARD DELETE
def test_hard_delete_set_authenticated_valid_set(setup_mock_data):
    pass

def test_hard_delete_set_authenticated_set_does_not_exist(setup_mock_data):
    pass

def test_hard_delete_set_authenticated_set_belongs_to_another_user(setup_mock_data):
    pass

def test_hard_delete_set_not_authenticated(setup_mock_data):
    pass

############## GET ALL
def test_hard_get_sets_authenticated(setup_mock_data):
    pass

def test_hard_get_sets_not_authenticated(setup_mock_data):
    pass

##################################################################################################### USER TABLE

############## SIGNUP
