/**
 * Equai AI - Main Application Component
 * Full-stack AI-powered math solver with step-by-step explanations
 */
import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import { solveProblem } from './services/api';

function App() {
  // State management
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handle sending message (like ChatGPT)
   */
  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const result = await solveProblem(input);
      
      const aiMessage = {
        role: 'assistant',
        content: result,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Error:', err);
      const errorMessage = {
        role: 'assistant',
        content: { 
          error: err.response?.data?.error || 'An error occurred. Please try again.'
        },
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle Enter key press
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-dark-bg">
      <Header />
      
      {/* Chat Container */}
      <main className="flex-1 overflow-hidden flex flex-col max-w-4xl w-full mx-auto">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-accent rounded-2xl flex items-center justify-center mb-6">
                <span className="text-4xl">🧠</span>
              </div>
              <h2 className="text-3xl font-montserrat font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Equai AI Math Solver
              </h2>
              <p className="text-gray-400 max-w-md mb-8">
                Ask me any math problem! I'll solve it and explain every step.
              </p>
              <div className="grid grid-cols-2 gap-3 max-w-lg">
                <button
                  onClick={() => setInput('What is 25% of 80?')}
                  className="p-4 bg-dark-card border border-dark-border rounded-lg hover:border-accent transition-all text-left"
                >
                  <p className="text-sm text-gray-400 mb-1">💰 Percentage</p>
                  <p className="text-white text-sm">What is 25% of 80?</p>
                </button>
                <button
                  onClick={() => setInput('x^2 - 5x + 6 = 0')}
                  className="p-4 bg-dark-card border border-dark-border rounded-lg hover:border-accent transition-all text-left"
                >
                  <p className="text-sm text-gray-400 mb-1">📐 Algebra</p>
                  <p className="text-white text-sm">x² - 5x + 6 = 0</p>
                </button>
                <button
                  onClick={() => setInput('sin(45)')}
                  className="p-4 bg-dark-card border border-dark-border rounded-lg hover:border-accent transition-all text-left"
                >
                  <p className="text-sm text-gray-400 mb-1">📊 Trigonometry</p>
                  <p className="text-white text-sm">sin(45)</p>
                </button>
                <button
                  onClick={() => setInput('sqrt(144)')}
                  className="p-4 bg-dark-card border border-dark-border rounded-lg hover:border-accent transition-all text-left"
                >
                  <p className="text-sm text-gray-400 mb-1">🔢 Roots</p>
                  <p className="text-white text-sm">√144</p>
                </button>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))
          )}
          
          {loading && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-sm">🧠</span>
              </div>
              <div className="flex-1 bg-dark-card border border-dark-border rounded-2xl p-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                  <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                  <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area (Fixed at bottom like ChatGPT) */}
        <div className="border-t border-dark-border p-4 bg-dark-bg">
          <div className="flex items-end space-x-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me any math problem..."
              className="flex-1 bg-dark-card border border-dark-border rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent resize-none max-h-32"
              rows="1"
              style={{
                minHeight: '48px',
                height: 'auto'
              }}
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className={`p-3 rounded-xl transition-all ${
                loading || !input.trim()
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-gradient-to-r from-primary to-accent hover:shadow-lg hover:shadow-accent/50'
              }`}
            >
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Press Enter to send • Shift+Enter for new line
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;
