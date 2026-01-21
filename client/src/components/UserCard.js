import React from 'react';
import { useNavigate } from 'react-router-dom';
import SimilarityIndicator from './SimilarityIndicator';

/**
 * UserCard component displays a summary of user information in a card format
 * @param {Object} user - User object with all user data
 */
const UserCard = ({ user }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/users/${user.id}`);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div
      onClick={handleClick}
      className="bg-white rounded-xl border border-gray-100 hover:border-primary-200 hover:shadow-lg transition-all duration-300 cursor-pointer p-6 shadow-sm"
    >
      <div className="flex justify-between items-start mb-5">
        <div>
          <h3 className="text-xl font-light text-gray-900 mb-2">
            {user.name || 'N/A'}
          </h3>
          <p className="text-sm text-gray-400">{user.email || 'N/A'}</p>
        </div>
        {user.similarity_score !== undefined && (
          <span className="px-3 py-1 bg-primary-50 text-primary-600 text-xs font-normal rounded-full border border-primary-100">
            Match
          </span>
        )}
      </div>

      <div className="space-y-3 mb-5">
        <div>
          <span className="text-xs font-normal text-gray-400 uppercase tracking-wide">Profession</span>
          <p className="text-sm text-gray-700 mt-1.5 font-light">{user.profession || 'N/A'}</p>
        </div>
        <div>
          <span className="text-xs font-normal text-gray-400 uppercase tracking-wide">Location</span>
          <p className="text-sm text-gray-700 mt-1.5 font-light">{user.location || 'N/A'}</p>
        </div>
        <div>
          <span className="text-xs font-normal text-gray-400 uppercase tracking-wide">Added</span>
          <p className="text-sm text-gray-700 mt-1.5 font-light">{formatDate(user.created_date)}</p>
        </div>
      </div>

      {user.similarity_score !== undefined && (
        <div className="mt-5 pt-5 border-t border-gray-100">
          <SimilarityIndicator similarityScore={user.similarity_score} />
        </div>
      )}
    </div>
  );
};

export default UserCard;
