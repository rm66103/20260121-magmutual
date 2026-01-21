"""
CSV Reader Module

Loads and parses user data from CSV file.
Caches data in memory to avoid re-reading on each request.
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Cache for loaded CSV data
_cached_data: Optional[List[Dict[str, any]]] = None


def load_users(csv_path: Optional[str] = None) -> List[Dict[str, any]]:
    """
    Load users from CSV file and cache in memory.
    
    Args:
        csv_path: Optional path to CSV file. Defaults to api/data/users.csv
        
    Returns:
        List of dictionaries containing user data
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV parsing fails
    """
    global _cached_data
    
    # Return cached data if available
    if _cached_data is not None:
        return _cached_data
    
    # Default path
    if csv_path is None:
        csv_path = Path(__file__).parent / 'data' / 'users.csv'
    else:
        csv_path = Path(csv_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    users = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse created_date string to date object for filtering
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
                        pass  # Keep as string if conversion fails
                
                users.append(row)
        
        # Cache the data
        _cached_data = users
        return users
        
    except csv.Error as e:
        raise ValueError(f"Error parsing CSV file: {e}") from e


def get_user_by_id(user_id: str) -> Optional[Dict[str, any]]:
    """
    Get a single user by ID.
    
    Args:
        user_id: User ID to search for
        
    Returns:
        User dictionary if found, None otherwise
    """
    users = load_users()
    for user in users:
        if user.get('id') == str(user_id):
            return user
    return None


def clear_cache():
    """Clear the cached CSV data (useful for testing)."""
    global _cached_data
    _cached_data = None
