"""
FastAPI Application

Main API endpoints for user data queries.
"""
from datetime import date
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .csv_reader import load_users, get_user_by_id
from .vector_search import initialize_vector_db, search_similar_professions

app = FastAPI(title="User API", description="API for querying user data from CSV")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data on startup
@app.on_event("startup")
async def startup_event():
    """Load CSV data and initialize vector database on application startup."""
    users = load_users()
    initialize_vector_db(users)
    print(f"Loaded {len(users)} users and initialized vector search")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "User API",
        "endpoints": {
            "GET /users/{user_id}": "Get a specific user by ID",
            "GET /users": "Get users with optional filters (start_date, end_date, profession)",
            "GET /users/search": "Semantic search for users by profession (with optional date filters)"
        }
    }


@app.get("/users/search")
async def search_users_by_profession(
    profession: str = Query(..., description="Profession text to search for semantically"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results to return"),
    start_date: Optional[str] = Query(None, description="Filter users created on/after this date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter users created on/before this date (YYYY-MM-DD)")
):
    """
    Semantic search for users by profession using vector similarity.
    
    Query Parameters:
        profession: Profession text to search for (required)
        limit: Maximum number of results (default: 10, max: 100)
        start_date: Filter users created on/after this date (YYYY-MM-DD)
        end_date: Filter users created on/before this date (YYYY-MM-DD)
        
    Returns:
        List of user objects ordered by similarity score, with similarity_score included
    """
    # Parse date strings if provided
    start_date_obj = None
    end_date_obj = None
    
    if start_date:
        try:
            start_date_obj = date.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid start_date format. Use YYYY-MM-DD")
    
    if end_date:
        try:
            end_date_obj = date.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid end_date format. Use YYYY-MM-DD")
    
    # Search for similar professions (fetch more results to account for date filtering)
    try:
        search_results = search_similar_professions(profession, limit=limit * 2)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Vector search error: {str(e)}")
    
    # Get full user records from CSV
    users = load_users()
    user_dict = {user['id']: user for user in users}
    
    # Build response with full user data and similarity scores, applying date filters
    results = []
    for user_id, similarity_score, profession_text in search_results:
        if user_id in user_dict:
            user = user_dict[user_id].copy()
            
            # Apply date filters
            if start_date_obj and user.get('created_date'):
                if user['created_date'] < start_date_obj:
                    continue
            
            if end_date_obj and user.get('created_date'):
                if user['created_date'] > end_date_obj:
                    continue
            
            # Convert date to string for JSON
            if 'created_date' in user and hasattr(user['created_date'], 'isoformat'):
                user['created_date'] = user['created_date'].isoformat()
            # Add similarity score
            user['similarity_score'] = round(similarity_score, 4)
            results.append(user)
            
            if len(results) >= limit:
                break
    
    return results


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """
    Get a specific user by ID.
    
    Args:
        user_id: User ID to retrieve
        
    Returns:
        User object with all fields from CSV
        
    Raises:
        404: If user not found
    """
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Convert date object back to string for JSON serialization
    if 'created_date' in user and hasattr(user['created_date'], 'isoformat'):
        user = user.copy()
        user['created_date'] = user['created_date'].isoformat()
    
    return user


@app.get("/users")
async def get_users(
    start_date: Optional[str] = Query(None, description="Filter users created on/after this date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter users created on/before this date (YYYY-MM-DD)"),
    profession: Optional[str] = Query(None, description="Filter by exact profession match")
):
    """
    Get list of users with optional filters.
    
    Query Parameters:
        start_date: Filter users created on/after this date (YYYY-MM-DD)
        end_date: Filter users created on/before this date (YYYY-MM-DD)
        profession: Filter by exact profession match
        
    Returns:
        List of user objects matching the filters
    """
    users = load_users()
    
    # Parse date strings if provided
    start_date_obj = None
    end_date_obj = None
    
    if start_date:
        try:
            start_date_obj = date.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid start_date format. Use YYYY-MM-DD")
    
    if end_date:
        try:
            end_date_obj = date.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid end_date format. Use YYYY-MM-DD")
    
    # Apply filters
    filtered_users = []
    for user in users:
        # Date range filter
        if start_date_obj and user.get('created_date'):
            if user['created_date'] < start_date_obj:
                continue
        
        if end_date_obj and user.get('created_date'):
            if user['created_date'] > end_date_obj:
                continue
        
        # Profession filter (exact match)
        if profession:
            if user.get('profession', '').lower() != profession.lower():
                continue
        
        filtered_users.append(user)
    
    # Convert date objects to strings for JSON serialization
    result = []
    for user in filtered_users:
        user_copy = user.copy()
        if 'created_date' in user_copy and hasattr(user_copy['created_date'], 'isoformat'):
            user_copy['created_date'] = user_copy['created_date'].isoformat()
        result.append(user_copy)
    
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
