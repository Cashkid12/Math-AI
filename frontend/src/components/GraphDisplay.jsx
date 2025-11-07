/**
 * Graph Display Component
 * Shows mathematical function graphs
 */
import React from 'react';
import { getGraphUrl } from '../services/api';

const GraphDisplay = ({ graphUrl }) => {
  if (!graphUrl) {
    return null;
  }

  const fullUrl = getGraphUrl(graphUrl);

  return (
    <div className="bg-dark-card border border-dark-border rounded-2xl p-6">
      <h3 className="text-xl font-montserrat font-bold text-white mb-4 flex items-center">
        <svg className="w-6 h-6 mr-2 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
        </svg>
        Graph Visualization
      </h3>
      <div className="bg-dark-bg rounded-lg p-4 flex justify-center items-center">
        <img 
          src={fullUrl} 
          alt="Mathematical Graph" 
          className="max-w-full h-auto rounded-lg shadow-lg"
          onError={(e) => {
            e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%231A1F2E" width="400" height="300"/%3E%3Ctext fill="%23ffffff" x="50%25" y="50%25" text-anchor="middle" dominant-baseline="middle"%3EGraph could not be loaded%3C/text%3E%3C/svg%3E';
          }}
        />
      </div>
    </div>
  );
};

export default GraphDisplay;
