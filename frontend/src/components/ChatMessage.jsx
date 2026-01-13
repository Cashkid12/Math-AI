/**
 * ChatMessage Component - ChatGPT-style message display
 * Shows user messages and AI responses with special sections for graphs
 */
import React from 'react';
import GraphDisplay from './GraphDisplay';

const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';
  const content = message.content;

  if (isUser) {
    // User message
    return (
      <div className="flex items-start space-x-3 justify-end">
        <div className="bg-black text-white rounded-2xl px-4 py-3 max-w-2xl">
          <p className="whitespace-pre-wrap">{content}</p>
        </div>
        <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-sm text-white">👤</span>
        </div>
      </div>
    );
  }

  // AI message
  if (content.error) {
    return (
      <div className="flex items-start space-x-3">
        <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-sm text-white">∑</span>
        </div>
        <div className="flex-1 bg-white border border-black rounded-2xl p-4 max-w-2xl">
          <p className="text-red-600">{content.error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start space-x-3">
      <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0">
        <span className="text-sm text-white">∑</span>
      </div>
      <div className="flex-1 space-y-4 max-w-3xl">
        {/* Problem Type Badge */}
        {content.problem_type && (
          <div className="inline-block px-3 py-1 bg-gray-100 border border-black rounded-full text-sm">
            <span className="text-black font-semibold">{content.problem_type}</span>
          </div>
        )}

        {/* Solution Box */}
        <div className="bg-white border border-black rounded-2xl p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-black mb-2">Solution</h3>
            <div className="bg-gray-100 rounded-lg p-4">
              <p className="text-2xl font-mono text-black">
                {typeof content.solution === 'object' 
                  ? JSON.stringify(content.solution) 
                  : content.solution}
              </p>
            </div>
          </div>

          {/* Step-by-Step Explanation */}
          {content.detailed_steps && content.detailed_steps.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Step-by-Step
              </h3>
              <div className="space-y-3">
                {content.detailed_steps.map((item, index) => (
                  <div 
                    key={index} 
                    className="bg-gray-100 rounded-lg p-4 border-l-4 border-black"
                  >
                    <div className="flex items-start">
                      <div className="flex-shrink-0 w-6 h-6 bg-black rounded-full flex items-center justify-center mr-3 mt-1">
                        <span className="text-white font-bold text-xs">{index + 1}</span>
                      </div>
                      <div className="flex-1">
                        <p className="text-black font-mono mb-2">{item.step}</p>
                        {item.explanation && (
                          <p className="text-gray-600 text-sm italic">{item.explanation}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Additional Forms (expanded, factored, etc.) */}
          {content.forms && (
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-3">
              {content.forms.simplified && (
                <div className="bg-gray-100 rounded-lg p-3">
                  <p className="text-xs text-gray-600 mb-1">Simplified</p>
                  <p className="text-black font-mono text-sm">{content.forms.simplified}</p>
                </div>
              )}
              {content.forms.expanded && (
                <div className="bg-gray-100 rounded-lg p-3">
                  <p className="text-xs text-gray-600 mb-1">Expanded</p>
                  <p className="text-black font-mono text-sm">{content.forms.expanded}</p>
                </div>
              )}
              {content.forms.factored && (
                <div className="bg-gray-100 rounded-lg p-3">
                  <p className="text-xs text-gray-600 mb-1">Factored</p>
                  <p className="text-black font-mono text-sm">{content.forms.factored}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Graph Section (Separate Card) */}
        {content.graph_url && (
          <div className="bg-white border border-black rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-black mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
              Graph Visualization
            </h3>
            <GraphDisplay graphUrl={content.graph_url} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
