"""
Vector Search Module

Handles semantic similarity search for professions using sentence-transformers and in-memory cosine similarity.
Uses numpy/scipy for similarity calculations - no SQLite extensions required.
"""
from typing import List, Tuple, Optional, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import cosine

# Global variables for model and embeddings
_model: Optional[SentenceTransformer] = None
_embeddings: Dict[str, np.ndarray] = {}  # user_id -> embedding
_professions: Dict[str, str] = {}  # user_id -> profession text


def initialize_vector_db(csv_data: List[dict], db_path: Optional[str] = None) -> None:
    """
    Initialize in-memory vector embeddings for all professions.
    
    Args:
        csv_data: List of user dictionaries from CSV
        db_path: Ignored (kept for API compatibility)
    """
    global _model, _embeddings, _professions
    
    # Initialize sentence-transformers model (downloads on first use)
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Clear existing data
    _embeddings.clear()
    _professions.clear()
    
    # Collect professions to embed
    professions_to_embed = []
    user_ids = []
    profession_texts = []
    
    for user in csv_data:
        profession = user.get('profession', '')
        user_id = user.get('id', '')
        if profession and user_id:
            professions_to_embed.append(profession)
            user_ids.append(user_id)
            profession_texts.append(profession)
    
    if professions_to_embed:
        # Generate embeddings in batch
        embeddings = _model.encode(professions_to_embed, show_progress_bar=False)
        
        # Store in memory
        for embedding, profession, user_id in zip(embeddings, profession_texts, user_ids):
            _embeddings[user_id] = embedding
            _professions[user_id] = profession


def search_similar_professions(query_profession: str, limit: int = 10) -> List[Tuple[str, float, str]]:
    """
    Search for similar professions using vector similarity.
    
    Args:
        query_profession: Profession text to search for
        limit: Maximum number of results to return
        
    Returns:
        List of tuples: (user_id, similarity_score, profession) ordered by relevance
        Similarity scores are cosine similarity (higher is more similar, range 0-1)
    """
    global _model, _embeddings, _professions
    
    if _model is None or not _embeddings:
        raise RuntimeError("Vector database not initialized. Call initialize_vector_db() first.")
    
    # Generate embedding for query
    query_embedding = _model.encode([query_profession], show_progress_bar=False)[0]
    
    # Calculate cosine similarity with all stored embeddings
    similarities = []
    for user_id, embedding in _embeddings.items():
        # Cosine similarity: 1 - cosine_distance
        # cosine() returns distance (0 = identical, 2 = opposite)
        # similarity = 1 - (distance / 2) gives us 1 = identical, 0 = opposite
        distance = cosine(query_embedding, embedding)
        similarity = 1.0 - (distance / 2.0)
        similarities.append((user_id, similarity, _professions[user_id]))
    
    # Sort by similarity (descending) and return top results
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:limit]


def close_connection():
    """Clear the in-memory embeddings (useful for testing)."""
    global _embeddings, _professions
    _embeddings.clear()
    _professions.clear()
