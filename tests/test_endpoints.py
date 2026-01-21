"""
Tests for API endpoints.
"""
import pytest
import tempfile
import csv
from pathlib import Path
from fastapi.testclient import TestClient

from api.main import app
from api.csv_reader import clear_cache
from api.vector_search import close_connection


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear all caches before each test."""
    clear_cache()
    close_connection()
    yield
    # Cleanup after test
    clear_cache()
    close_connection()


@pytest.fixture
def sample_csv_data():
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email', 'profession', 'created_date', 'age', 'location', 'phone'])
        writer.writeheader()
        # Add diverse professions for semantic search testing
        writer.writerow({
            'id': '1',
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'profession': 'Software Engineer',
            'created_date': '2023-01-15',
            'age': '30',
            'location': 'New York, NY',
            'phone': '555-1234'
        })
        writer.writerow({
            'id': '2',
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'profession': 'Software Developer',
            'created_date': '2023-06-20',
            'age': '28',
            'location': 'San Francisco, CA',
            'phone': '555-5678'
        })
        writer.writerow({
            'id': '3',
            'name': 'Bob Johnson',
            'email': 'bob.johnson@example.com',
            'profession': 'Doctor',
            'created_date': '2022-03-10',
            'age': '45',
            'location': 'Boston, MA',
            'phone': '555-9012'
        })
        writer.writerow({
            'id': '4',
            'name': 'Alice Williams',
            'email': 'alice.williams@example.com',
            'profession': 'Physician',
            'created_date': '2023-09-05',
            'age': '38',
            'location': 'Chicago, IL',
            'phone': '555-3456'
        })
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()
    clear_cache()
    close_connection()


@pytest.fixture
def client(sample_csv_data, monkeypatch):
    """Create a test client with sample data."""
    # Clear cache first
    clear_cache()
    close_connection()
    
    # Import modules to patch
    import api.csv_reader
    import api.main
    
    # Create a mock that completely bypasses cache and loads directly from test CSV
    def mock_load_users(csv_path=None):
        # Always use test CSV when no path is specified
        if csv_path is None:
            csv_path = sample_csv_data
        
        # Bypass cache completely - load directly from file
        from pathlib import Path
        import csv
        from datetime import datetime
        
        csv_path = Path(csv_path)
        users = []
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse created_date string to date object
                if 'created_date' in row and row['created_date']:
                    try:
                        row['created_date'] = datetime.strptime(row['created_date'], '%Y-%m-%d').date()
                    except ValueError as e:
                        raise ValueError(f"Invalid date format in CSV: {row.get('created_date')}") from e
                
                # Ensure age is an integer
                if 'age' in row and row['age']:
                    try:
                        row['age'] = int(row['age'])
                    except ValueError:
                        pass
                
                users.append(row)
        
        return users
    
    # Patch BOTH where it's defined AND where it's imported/used
    # This is critical: api.main imports load_users, so we need to patch both
    monkeypatch.setattr(api.csv_reader, 'load_users', mock_load_users)
    monkeypatch.setattr(api.main, 'load_users', mock_load_users)
    monkeypatch.setattr(api.csv_reader, '_cached_data', None)
    
    # Use TestClient with context manager to ensure startup events run properly
    # This also ensures the patched function is used during startup
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_get_user_by_id(client):
    """Test getting a user by ID."""
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == '1'
    assert data['name'] == 'John Doe'
    assert data['profession'] == 'Software Engineer'
    assert data['created_date'] == '2023-01-15'


def test_get_user_by_id_not_found(client):
    """Test getting a non-existent user."""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_users_no_filters(client):
    """Test getting all users without filters."""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4


def test_get_users_filter_by_start_date(client):
    """Test filtering users by start_date."""
    response = client.get("/users?start_date=2023-06-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Only users created on/after June 1, 2023
    assert all(user['created_date'] >= '2023-06-01' for user in data)


def test_get_users_filter_by_end_date(client):
    """Test filtering users by end_date."""
    response = client.get("/users?end_date=2023-01-31")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Users created before/on Jan 31, 2023: User 1 (2023-01-15) and User 3 (2022-03-10)
    user_ids = [user['id'] for user in data]
    assert '1' in user_ids  # 2023-01-15
    assert '3' in user_ids  # 2022-03-10
    assert all(user['created_date'] <= '2023-01-31' for user in data)


def test_get_users_filter_by_date_range(client):
    """Test filtering users by date range."""
    response = client.get("/users?start_date=2023-01-01&end_date=2023-06-30")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Users created between Jan 1 and June 30, 2023: User 1 (2023-01-15) and User 2 (2023-06-20)
    user_ids = [user['id'] for user in data]
    assert '1' in user_ids  # 2023-01-15
    assert '2' in user_ids  # 2023-06-20
    assert all('2023-01-01' <= user['created_date'] <= '2023-06-30' for user in data)


def test_get_users_filter_by_profession(client):
    """Test filtering users by exact profession match."""
    response = client.get("/users?profession=Software Engineer")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['profession'] == 'Software Engineer'


def test_get_users_filter_by_profession_case_insensitive(client):
    """Test that profession filter is case-insensitive."""
    response = client.get("/users?profession=software engineer")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['profession'] == 'Software Engineer'


def test_get_users_invalid_date_format(client):
    """Test filtering with invalid date format."""
    response = client.get("/users?start_date=invalid-date")
    assert response.status_code == 400
    assert "Invalid" in response.json()["detail"]


def test_search_users_by_profession(client):
    """Test semantic search for users by profession."""
    response = client.get("/users/search?profession=programmer")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Should find Software Engineer and Software Developer (semantically similar)
    professions = [user['profession'] for user in data]
    assert 'Software Engineer' in professions or 'Software Developer' in professions
    # Check that similarity scores are included
    assert 'similarity_score' in data[0]


def test_search_users_by_profession_limit(client):
    """Test semantic search with limit parameter."""
    response = client.get("/users/search?profession=doctor&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2
    # Should find Doctor and Physician (semantically similar)
    professions = [user['profession'] for user in data]
    assert 'Doctor' in professions or 'Physician' in professions


def test_search_users_by_profession_required_parameter(client):
    """Test that profession parameter is required for search."""
    response = client.get("/users/search")
    assert response.status_code == 422  # Validation error


def test_search_users_by_profession_limit_validation(client):
    """Test that limit parameter is validated."""
    response = client.get("/users/search?profession=engineer&limit=0")
    assert response.status_code == 422  # Validation error (limit must be >= 1)
    
    response = client.get("/users/search?profession=engineer&limit=101")
    assert response.status_code == 422  # Validation error (limit must be <= 100)


def test_search_users_by_profession_with_start_date(client):
    """Test semantic search with start_date filter."""
    response = client.get("/users/search?profession=programmer&start_date=2023-06-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # All results should be on/after the start date
    for user in data:
        if user.get('created_date'):
            assert user['created_date'] >= '2023-06-01'


def test_search_users_by_profession_with_end_date(client):
    """Test semantic search with end_date filter."""
    response = client.get("/users/search?profession=doctor&end_date=2023-01-31")
    assert response.status_code == 200
    data = response.json()
    # All results should be on/before the end date
    for user in data:
        if user.get('created_date'):
            assert user['created_date'] <= '2023-01-31'


def test_search_users_by_profession_with_date_range(client):
    """Test semantic search with both start_date and end_date filters."""
    response = client.get("/users/search?profession=engineer&start_date=2023-01-01&end_date=2023-06-30")
    assert response.status_code == 200
    data = response.json()
    # All results should be within the date range
    for user in data:
        if user.get('created_date'):
            assert '2023-01-01' <= user['created_date'] <= '2023-06-30'


def test_search_users_by_profession_invalid_date_format(client):
    """Test semantic search with invalid date format."""
    response = client.get("/users/search?profession=engineer&start_date=invalid-date")
    assert response.status_code == 400
    assert "Invalid" in response.json()["detail"]
