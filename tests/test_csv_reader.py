"""
Tests for CSV reader module.
"""
import pytest
import tempfile
import csv
from pathlib import Path
from datetime import date

from api.csv_reader import load_users, get_user_by_id, clear_cache


@pytest.fixture
def sample_csv_file():
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email', 'profession', 'created_date', 'age', 'location', 'phone'])
        writer.writeheader()
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
            'profession': 'Data Scientist',
            'created_date': '2023-06-20',
            'age': '28',
            'location': 'San Francisco, CA',
            'phone': '555-5678'
        })
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()
    clear_cache()


def test_load_users(sample_csv_file):
    """Test loading users from CSV file."""
    clear_cache()
    users = load_users(sample_csv_file)
    
    assert len(users) == 2
    assert users[0]['id'] == '1'
    assert users[0]['name'] == 'John Doe'
    assert users[0]['profession'] == 'Software Engineer'
    assert isinstance(users[0]['created_date'], date)
    assert users[0]['created_date'] == date(2023, 1, 15)
    assert users[0]['age'] == 30


def test_load_users_caching(sample_csv_file):
    """Test that CSV data is cached after first load."""
    clear_cache()
    users1 = load_users(sample_csv_file)
    users2 = load_users(sample_csv_file)
    
    # Should return same list object (cached)
    assert users1 is users2


def test_get_user_by_id(sample_csv_file, monkeypatch):
    """Test getting a user by ID."""
    clear_cache()
    
    # Monkeypatch load_users to use test CSV
    import api.csv_reader
    original_load = api.csv_reader.load_users
    
    def mock_load_users(csv_path=None):
        if csv_path is None:
            return original_load(sample_csv_file)
        return original_load(csv_path)
    
    monkeypatch.setattr(api.csv_reader, 'load_users', mock_load_users)
    clear_cache()
    
    user = get_user_by_id('1')
    
    assert user is not None
    assert user['id'] == '1'
    assert user['name'] == 'John Doe'


def test_get_user_by_id_not_found(sample_csv_file, monkeypatch):
    """Test getting a non-existent user ID."""
    clear_cache()
    
    # Monkeypatch load_users to use test CSV
    import api.csv_reader
    original_load = api.csv_reader.load_users
    
    def mock_load_users(csv_path=None):
        if csv_path is None:
            return original_load(sample_csv_file)
        return original_load(csv_path)
    
    monkeypatch.setattr(api.csv_reader, 'load_users', mock_load_users)
    clear_cache()
    
    user = get_user_by_id('999')
    
    assert user is None


def test_load_users_file_not_found():
    """Test loading users from non-existent file."""
    clear_cache()
    with pytest.raises(FileNotFoundError):
        load_users('/nonexistent/file.csv')


def test_load_users_invalid_date():
    """Test loading CSV with invalid date format."""
    clear_cache()
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email', 'profession', 'created_date', 'age', 'location', 'phone'])
        writer.writeheader()
        writer.writerow({
            'id': '1',
            'name': 'Test User',
            'email': 'test@example.com',
            'profession': 'Engineer',
            'created_date': 'invalid-date',
            'age': '30',
            'location': 'NYC',
            'phone': '555-0000'
        })
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="Invalid date format"):
            load_users(temp_path)
    finally:
        Path(temp_path).unlink()
        clear_cache()
