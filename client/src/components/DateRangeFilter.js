import React from 'react';

/**
 * DateRangeFilter component for filtering users by date range
 * @param {string} startDate - Start date value (YYYY-MM-DD)
 * @param {string} endDate - End date value (YYYY-MM-DD)
 * @param {Function} onStartDateChange - Callback when start date changes
 * @param {Function} onEndDateChange - Callback when end date changes
 * @param {Function} onClear - Callback to clear all filters
 */
const DateRangeFilter = ({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  onClear,
}) => {
  const hasFilters = startDate || endDate;

  return (
    <div className="space-y-5">
      <div className="flex gap-4 items-end">
        <div className="flex-1">
          <label htmlFor="start-date" className="block text-xs font-normal text-gray-400 uppercase tracking-wide mb-2">
            Start Date
          </label>
          <input
            id="start-date"
            type="date"
            value={startDate || ''}
            onChange={(e) => onStartDateChange(e.target.value)}
            className="w-full px-5 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-200 focus:border-primary-300 outline-none text-gray-700 bg-gray-50 hover:bg-white transition-colors duration-200"
          />
        </div>
        <div className="flex-1">
          <label htmlFor="end-date" className="block text-xs font-normal text-gray-400 uppercase tracking-wide mb-2">
            End Date
          </label>
          <input
            id="end-date"
            type="date"
            value={endDate || ''}
            onChange={(e) => onEndDateChange(e.target.value)}
            className="w-full px-5 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-200 focus:border-primary-300 outline-none text-gray-700 bg-gray-50 hover:bg-white transition-colors duration-200"
          />
        </div>
        {hasFilters && (
          <button
            type="button"
            onClick={onClear}
            className="px-5 py-3 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200 transition-colors duration-200 font-light text-sm whitespace-nowrap border border-gray-200"
          >
            Clear Dates
          </button>
        )}
      </div>
      <p className="text-xs text-gray-400 font-light">
        Filter candidates by when they were added to the system
      </p>
    </div>
  );
};

export default DateRangeFilter;
