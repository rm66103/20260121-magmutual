import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getUserById } from '../services/api';
import SimilarityIndicator from '../components/SimilarityIndicator';

const UserDetailView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadUser = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getUserById(id);
      setUser(data);
    } catch (err) {
      setError(err.response?.status === 404 
        ? 'Candidate not found' 
        : 'Failed to load candidate details. Please try again.');
      console.error('Error loading user:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-500"></div>
          <p className="mt-6 text-gray-500 text-lg font-light">Loading candidate details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-xl border border-gray-100 p-10 text-center shadow-sm">
          <p className="text-red-500 font-light mb-6 text-lg">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-all duration-200 font-light text-sm shadow-sm hover:shadow-md"
          >
            Back to Candidates
          </button>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <button
            onClick={() => navigate('/')}
            className="text-primary-600 hover:text-primary-700 font-light flex items-center gap-2 text-sm transition-colors duration-200"
          >
            <span>←</span> Back to Candidates
          </button>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl border border-gray-100 p-10 shadow-sm">
          {/* Header */}
          <div className="border-b border-gray-100 pb-8 mb-8">
            <h1 className="text-4xl font-light text-gray-900 mb-3">{user.name || 'N/A'}</h1>
            <p className="text-xl text-gray-500 font-light">{user.profession || 'N/A'}</p>
          </div>

          {/* Similarity Score (if present) */}
          {user.similarity_score !== undefined && (
            <div className="mb-8 pb-8 border-b border-gray-100">
              <SimilarityIndicator similarityScore={user.similarity_score} />
            </div>
          )}

          {/* User Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            <div>
              <h3 className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-6">
                Contact Information
              </h3>
              <dl className="space-y-5">
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Email</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">
                    <a
                      href={`mailto:${user.email}`}
                      className="text-primary-600 hover:text-primary-700 transition-colors duration-200"
                    >
                      {user.email || 'N/A'}
                    </a>
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Phone</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">
                    <a
                      href={`tel:${user.phone}`}
                      className="text-primary-600 hover:text-primary-700 transition-colors duration-200"
                    >
                      {user.phone || 'N/A'}
                    </a>
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Location</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">{user.location || 'N/A'}</dd>
                </div>
              </dl>
            </div>

            <div>
              <h3 className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-6">
                Profile Information
              </h3>
              <dl className="space-y-5">
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Profession</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">{user.profession || 'N/A'}</dd>
                </div>
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Age</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">{user.age || 'N/A'}</dd>
                </div>
                <div>
                  <dt className="text-xs font-normal text-gray-400 uppercase tracking-wide mb-1.5">Date Added</dt>
                  <dd className="mt-1 text-sm text-gray-700 font-light">{formatDate(user.created_date)}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDetailView;
