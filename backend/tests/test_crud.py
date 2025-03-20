import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crud import crud, models, schemas # changed to absolute import
from database import Base, get_db # changed to absolute import

# ... (rest of your test code)

# Setup in memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    user_schema = schemas.UserCreate(username="testuser", email="test@example.com", password="password")
    user = crud.create_user(db=test_db, user=user_schema)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_get_user(test_db):
    user_schema = schemas.UserCreate(username="testuser", email="test@example.com", password="password")
    created_user = crud.create_user(db=test_db, user=user_schema)
    retrieved_user = crud.get_user(db=test_db, user_id=created_user.id)
    assert retrieved_user.username == "testuser"

# Add more tests for other CRUD functions (questions, discussions, etc.)
