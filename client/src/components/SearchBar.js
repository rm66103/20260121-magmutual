import React, { useState } from 'react';

/**
 * SearchBar component for profession search (semantic or exact match)
 * @param {Function} onSearch - Callback function called with search query and exact match flag
 */
const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [exactMatch, setExactMatch] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), exactMatch);
    }
  };

  const handleClear = () => {
    setQuery('');
    setExactMatch(false);
    onSearch('', false);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex gap-3">
        <div className="flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by profession (e.g., 'software engineer', 'doctor')..."
            className="w-full px-5 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-200 focus:border-primary-300 outline-none text-gray-700 placeholder-gray-400 bg-gray-50 hover:bg-white transition-colors duration-200"
          />
        </div>
        <button
          type="submit"
          className="px-8 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-all duration-200 font-light text-sm shadow-sm hover:shadow-md"
        >
          Search
        </button>
        {query && (
          <button
            type="button"
            onClick={handleClear}
            className="px-5 py-3 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200 transition-colors duration-200 font-light text-sm border border-gray-200"
          >
            Clear
          </button>
        )}
      </div>
      <div className="flex items-center gap-3 mt-3">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={exactMatch}
            onChange={(e) => setExactMatch(e.target.checked)}
            className="w-4 h-4 text-primary-500 border-gray-300 rounded focus:ring-primary-200 focus:ring-2"
          />
          <span className="text-sm text-gray-600 font-light">Exact match</span>
        </label>
        <p className="text-xs text-gray-400 font-light">
          {exactMatch 
            ? 'Find candidates with exact profession match'
            : 'Find candidates with similar professions using semantic search'}
        </p>
      </div>
    </form>
  );
};

export default SearchBar;
