/**
 * Header Component for Equai AI
 */
import React from 'react';

const Header = () => {
  return (
    <header className="bg-dark-card border-b border-dark-border sticky top-0 z-50 backdrop-blur-sm bg-opacity-95">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
              <span className="text-2xl font-bold text-white">∑</span>
            </div>
            <div>
              <h1 className="text-2xl font-montserrat font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Equai AI
              </h1>
              <p className="text-xs text-gray-400">Your Math Genius in an App</p>
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#solve" className="text-gray-300 hover:text-accent transition-colors duration-200">
              Solve
            </a>
            <a href="#history" className="text-gray-300 hover:text-accent transition-colors duration-200">
              History
            </a>
            <a href="#about" className="text-gray-300 hover:text-accent transition-colors duration-200">
              About
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
