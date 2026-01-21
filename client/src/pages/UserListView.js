import React, { useState, useEffect } from 'react';
import { getAllUsers, searchUsersByProfession } from '../services/api';
import UserCard from '../components/UserCard';
import SearchBar from '../components/SearchBar';
import DateRangeFilter from '../components/DateRangeFilter';

const UserListView = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [professionSearch, setProfessionSearch] = useState('');
  const [isSemanticSearch, setIsSemanticSearch] = useState(false);
  const [isExactMatch, setIsExactMatch] = useState(false);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const filters = {};
      if (startDate) filters.start_date = startDate;
      if (endDate) filters.end_date = endDate;
      
      const data = await getAllUsers(filters);
      setUsers(data);
      setIsSemanticSearch(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load users. Please try again.');
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // When date filters change, reload users or re-run search
    if (!professionSearch) {
      loadUsers();
    } else if (professionSearch) {
      // Re-run search with updated date filters
      handleProfessionSearch(professionSearch, isExactMatch);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [startDate, endDate]);

  const handleProfessionSearch = async (query, exactMatch = false) => {
    if (!query.trim()) {
      // Clear search - reload all users with date filters
      setProfessionSearch('');
      setIsSemanticSearch(false);
      setIsExactMatch(false);
      loadUsers();
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setProfessionSearch(query);
      setIsExactMatch(exactMatch);
      setIsSemanticSearch(!exactMatch);
      
      // Pass date filters to API
      const filters = {};
      if (startDate) filters.start_date = startDate;
      if (endDate) filters.end_date = endDate;
      
      let data;
      if (exactMatch) {
        // Use exact match endpoint
        filters.profession = query;
        data = await getAllUsers(filters);
      } else {
        // Use semantic search endpoint
        data = await searchUsersByProfession(query, 50, filters);
      }
      
      setUsers(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
      console.error('Error searching users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearDates = () => {
    setStartDate('');
    setEndDate('');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-light text-gray-900 mb-3">Candidate Database</h1>
          <p className="text-gray-500 text-lg">Search and filter through candidate profiles</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search and Filter Section */}
        <div className="bg-white rounded-xl border border-gray-100 p-8 mb-10 space-y-8 shadow-sm">
          <div>
            <h2 className="text-xl font-light text-gray-800 mb-5">Search by Profession</h2>
            <SearchBar onSearch={handleProfessionSearch} />
          </div>
          
          <div className="border-t border-gray-100 pt-8">
            <h2 className="text-xl font-light text-gray-800 mb-5">Filter by Date Range</h2>
            <DateRangeFilter
              startDate={startDate}
              endDate={endDate}
              onStartDateChange={setStartDate}
              onEndDateChange={setEndDate}
              onClear={handleClearDates}
            />
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-100 text-red-600 px-6 py-4 rounded-xl mb-8">
            <p className="font-medium mb-1">Error</p>
            <p className="text-sm text-red-500">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-16">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-500"></div>
            <p className="mt-6 text-gray-500 text-lg">Loading candidates...</p>
          </div>
        )}

        {/* Results */}
        {!loading && !error && (
          <>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-light text-gray-800">
                {users.length} {users.length === 1 ? 'Candidate' : 'Candidates'}
                {professionSearch && (
                  <span className="text-lg font-light text-gray-500 ml-3">
                    {isExactMatch ? 'exactly' : 'matching'} "{professionSearch}"
                  </span>
                )}
              </h2>
            </div>

            {users.length === 0 ? (
              <div className="bg-white rounded-xl border border-gray-100 p-16 text-center shadow-sm">
                <p className="text-gray-400 text-xl font-light">No candidates found</p>
                <p className="text-gray-300 text-base mt-3">
                  Try adjusting your search or filters
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {users.map((user) => (
                  <UserCard key={user.id} user={user} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default UserListView;
