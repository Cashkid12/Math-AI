/**
 * Input Component for Equai AI
 * Handles user input and problem type selection
 */
import React from 'react';

const ProblemInput = ({ 
  input, 
  setInput,
  onSolve,
  loading 
}) => {
  return (
    <div className="bg-dark-card border border-dark-border rounded-2xl p-8 shadow-2xl">
      <h2 className="text-2xl font-montserrat font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        ✨ Ask Me ANY Math Problem
      </h2>
      
      <p className="text-gray-400 mb-6 text-sm">
        I'm an AI math solver! Just type your problem in plain language or mathematical notation.
        I'll figure out what type it is and solve it for you.
      </p>
      
      {/* Input Field */}
      <div className="mb-6">
        <label className="block text-gray-300 mb-3 font-semibold">
          Your Math Problem
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Examples:
• 2 + 2
• x^2 + 5x + 6 = 0
• sin(30)
• derivative of x^3
• 15% of 200
• sqrt(16)
• 2^10"
          className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent resize-none transition-all duration-200"
          rows="5"
        />
      </div>
      
      {/* Solve Button */}
      <button
        onClick={onSolve}
        disabled={loading || !input.trim()}
        className={`w-full py-4 rounded-lg font-bold text-lg transition-all duration-200 ${
          loading || !input.trim()
            ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
            : 'bg-gradient-to-r from-primary to-accent text-white hover:shadow-lg hover:shadow-accent/50 transform hover:scale-[1.02] active:scale-[0.98]'
        }`}
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            AI is solving...
          </span>
        ) : (
          '🧠 Solve with AI'
        )}
      </button>
      
      {/* Quick Examples */}
      <div className="mt-6 p-4 bg-dark-bg rounded-lg border border-dark-border">
        <p className="text-sm text-gray-400 mb-2 font-semibold">🚀 Quick Examples - Click to try:</p>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setInput('2 + 2')}
            className="text-xs px-3 py-1 bg-dark-card border border-dark-border rounded-full text-accent hover:bg-accent hover:text-dark-bg transition-all duration-200"
          >
            2 + 2
          </button>
          <button
            onClick={() => setInput('x^2 - 4 = 0')}
            className="text-xs px-3 py-1 bg-dark-card border border-dark-border rounded-full text-accent hover:bg-accent hover:text-dark-bg transition-all duration-200"
          >
            x² - 4 = 0
          </button>
          <button
            onClick={() => setInput('sin(45)')}
            className="text-xs px-3 py-1 bg-dark-card border border-dark-border rounded-full text-accent hover:bg-accent hover:text-dark-bg transition-all duration-200"
          >
            sin(45)
          </button>
          <button
            onClick={() => setInput('sqrt(144)')}
            className="text-xs px-3 py-1 bg-dark-card border border-dark-border rounded-full text-accent hover:bg-accent hover:text-dark-bg transition-all duration-200"
          >
            √144
          </button>
          <button
            onClick={() => setInput('15% of 200')}
            className="text-xs px-3 py-1 bg-dark-card border border-dark-border rounded-full text-accent hover:bg-accent hover:text-dark-bg transition-all duration-200"
          >
            15% of 200
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProblemInput;
