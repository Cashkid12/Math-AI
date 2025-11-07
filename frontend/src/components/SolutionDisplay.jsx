/**
 * Solution Display Component
 * Shows detailed step-by-step solutions with explanations
 */
import React from 'react';

const SolutionDisplay = ({ solution, error }) => {
  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500/50 rounded-2xl p-6">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-semibold text-red-400">Error</h3>
            <p className="text-red-300 mt-2">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!solution) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Problem Type Badge */}
      {solution.problem_type && (
        <div className="flex justify-center">
          <span className="px-4 py-2 bg-gradient-to-r from-primary to-accent text-white rounded-full text-sm font-semibold">
            🧠 Detected: {solution.problem_type}
          </span>
        </div>
      )}

      {/* Solution Result */}
      <div className="bg-gradient-to-r from-primary/20 to-accent/20 border border-accent/30 rounded-2xl p-6">
        <h3 className="text-xl font-montserrat font-bold text-accent mb-3">
          ✓ Solution
        </h3>
        <div className="bg-dark-bg rounded-lg p-4">
          <p className="text-2xl font-semibold text-white font-mono">
            {typeof solution.solution === 'object' 
              ? JSON.stringify(solution.solution) 
              : solution.solution}
          </p>
        </div>
      </div>

      {/* Detailed Steps with Explanations */}
      {solution.detailed_steps && solution.detailed_steps.length > 0 && (
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6">
          <h3 className="text-xl font-montserrat font-bold text-white mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Step-by-Step Solution
          </h3>
          <div className="space-y-4">
            {solution.detailed_steps.map((item, index) => (
              <div 
                key={index} 
                className="bg-dark-bg rounded-lg p-4 border-l-4 border-accent hover:bg-opacity-80 transition-all duration-200"
              >
                {/* Step Number */}
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center mr-3">
                    <span className="text-dark-bg font-bold text-sm">{index + 1}</span>
                  </div>
                  <div className="flex-1">
                    {/* Mathematical Step */}
                    <div className="mb-2">
                      <p className="text-white font-mono text-lg">{item.step}</p>
                    </div>
                    {/* Explanation */}
                    {item.explanation && (
                      <div className="mt-2 pl-4 border-l-2 border-gray-600">
                        <p className="text-gray-300 text-sm italic">
                          💡 {item.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Traditional Steps (fallback) */}
      {solution.steps && !solution.detailed_steps && (
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6">
          <h3 className="text-xl font-montserrat font-bold text-white mb-4">
            Steps
          </h3>
          <div className="space-y-3">
            {solution.steps.map((step, index) => (
              <div key={index} className="flex items-start">
                <span className="text-accent font-bold mr-3">{index + 1}.</span>
                <p className="text-gray-300 font-mono">{step}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Additional Analysis (for graphs) */}
      {solution.analysis && (
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6">
          <h3 className="text-xl font-montserrat font-bold text-white mb-4">
            Function Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {solution.analysis.derivative && (
              <div className="bg-dark-bg rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Derivative</p>
                <p className="text-white font-mono">{solution.analysis.derivative}</p>
              </div>
            )}
            {solution.analysis.y_intercept && (
              <div className="bg-dark-bg rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Y-Intercept</p>
                <p className="text-white font-mono">{solution.analysis.y_intercept}</p>
              </div>
            )}
            {solution.analysis.critical_points && solution.analysis.critical_points.length > 0 && (
              <div className="bg-dark-bg rounded-lg p-4 md:col-span-2">
                <p className="text-gray-400 text-sm mb-1">Critical Points</p>
                <p className="text-white font-mono">
                  {solution.analysis.critical_points.join(', ')}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SolutionDisplay;
