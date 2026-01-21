import React from 'react';

/**
 * SimilarityIndicator component displays a progress bar showing semantic similarity match percentage
 * @param {number} similarityScore - Similarity score from 0 to 1
 */
const SimilarityIndicator = ({ similarityScore }) => {
  if (similarityScore === undefined || similarityScore === null) {
    return null;
  }

  const percentage = Math.round(similarityScore * 100);
  
  // Determine color based on similarity score - using primary blue tones
  let bgColor = 'bg-primary-500';
  let textColor = 'text-primary-600';
  
  if (percentage < 50) {
    bgColor = 'bg-red-400';
    textColor = 'text-red-500';
  } else if (percentage < 75) {
    bgColor = 'bg-primary-400';
    textColor = 'text-primary-500';
  }

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-normal text-gray-400 uppercase tracking-wide">Match Score</span>
        <span className={`text-sm font-light ${textColor}`}>
          {percentage}%
        </span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
        <div
          className={`h-2 ${bgColor} transition-all duration-500 ease-out rounded-full`}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin="0"
          aria-valuemax="100"
        />
      </div>
      <p className="text-xs text-gray-300 mt-2 font-light">
        Semantic similarity match based on profession
      </p>
    </div>
  );
};

export default SimilarityIndicator;
