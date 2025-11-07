"""
Graph Generation Module for Equai AI
Creates beautiful mathematical function graphs using Matplotlib
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import os
import logging
from config import Config

logger = logging.getLogger(__name__)

class GraphGenerator:
    """Generate graphs for mathematical functions"""
    
    def __init__(self):
        """Initialize graph generator"""
        self.x_symbol = sp.Symbol('x')
        self.transformations = (standard_transformations + 
                               (implicit_multiplication_application,))
        
        # Create graphs directory if it doesn't exist
        if not os.path.exists(Config.GRAPH_DIR):
            os.makedirs(Config.GRAPH_DIR)
    
    def parse_expression(self, expr_string):
        """Parse expression string to SymPy expression"""
        try:
            expr_string = expr_string.replace('^', '**')
            expr = parse_expr(expr_string, transformations=self.transformations)
            return expr
        except Exception as e:
            logger.error(f"Error parsing expression: {e}")
            raise ValueError(f"Could not parse expression: {expr_string}")
    
    def generate_graph(self, expr_string, xmin=-10, xmax=10, filename=None):
        """
        Generate a graph for the given expression
        
        Args:
            expr_string: Mathematical expression as string
            xmin: Minimum x value
            xmax: Maximum x value
            filename: Optional filename for the graph
            
        Returns:
            Path to saved graph image
        """
        try:
            # Parse expression
            expr = self.parse_expression(expr_string)
            
            # Convert to numerical function
            f = sp.lambdify(self.x_symbol, expr, 'numpy')
            
            # Generate x values
            x_vals = np.linspace(xmin, xmax, 1000)
            
            # Calculate y values with error handling
            try:
                y_vals = f(x_vals)
                # Handle potential infinities
                y_vals = np.where(np.abs(y_vals) > 1e10, np.nan, y_vals)
            except Exception as e:
                logger.warning(f"Error computing function values: {e}")
                # Try point by point
                y_vals = []
                for x in x_vals:
                    try:
                        y = float(f(x))
                        if abs(y) > 1e10:
                            y = np.nan
                        y_vals.append(y)
                    except:
                        y_vals.append(np.nan)
                y_vals = np.array(y_vals)
            
            # Create the plot with modern styling
            plt.figure(figsize=Config.GRAPH_FIGSIZE, dpi=Config.GRAPH_DPI)
            
            # Set dark theme colors
            bg_color = '#0E1117'
            grid_color = '#2E3440'
            line_color = '#00C896'
            text_color = '#FFFFFF'
            
            ax = plt.gca()
            ax.set_facecolor(bg_color)
            plt.gcf().patch.set_facecolor(bg_color)
            
            # Plot the function
            plt.plot(x_vals, y_vals, color=line_color, linewidth=2.5, label=f'f(x) = {expr}')
            
            # Add grid
            plt.grid(True, alpha=0.3, color=grid_color, linestyle='--')
            
            # Add axes
            plt.axhline(y=0, color=text_color, linewidth=0.8, alpha=0.5)
            plt.axvline(x=0, color=text_color, linewidth=0.8, alpha=0.5)
            
            # Styling
            plt.xlabel('x', fontsize=12, color=text_color, fontweight='bold')
            plt.ylabel('f(x)', fontsize=12, color=text_color, fontweight='bold')
            plt.title(f'Graph of f(x) = {expr}', fontsize=14, color=text_color, 
                     fontweight='bold', pad=20)
            
            # Set axis colors
            ax.spines['bottom'].set_color(text_color)
            ax.spines['top'].set_color(text_color)
            ax.spines['left'].set_color(text_color)
            ax.spines['right'].set_color(text_color)
            ax.tick_params(colors=text_color)
            
            # Add legend
            legend = plt.legend(facecolor=bg_color, edgecolor=grid_color, 
                              fontsize=10, loc='best')
            plt.setp(legend.get_texts(), color=text_color)
            
            # Set limits with some padding
            plt.xlim(xmin, xmax)
            
            # Auto-adjust y limits based on visible data
            valid_y = y_vals[~np.isnan(y_vals)]
            if len(valid_y) > 0:
                y_min, y_max = np.min(valid_y), np.max(valid_y)
                y_range = y_max - y_min
                if y_range > 0:
                    plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
            
            # Save the figure
            if filename is None:
                import hashlib
                filename = hashlib.md5(expr_string.encode()).hexdigest() + '.png'
            
            filepath = os.path.join(Config.GRAPH_DIR, filename)
            plt.tight_layout()
            plt.savefig(filepath, facecolor=bg_color, edgecolor='none', 
                       bbox_inches='tight', dpi=Config.GRAPH_DPI)
            plt.close()
            
            logger.info(f"Graph saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating graph: {e}")
            raise
    
    def generate_multi_graph(self, expressions, xmin=-10, xmax=10, filename=None):
        """
        Generate a graph with multiple functions
        
        Args:
            expressions: List of expression strings
            xmin: Minimum x value
            xmax: Maximum x value
            filename: Optional filename
            
        Returns:
            Path to saved graph image
        """
        try:
            colors = ['#00C896', '#1A73E8', '#FF6B6B', '#FFA500', '#9D4EDD']
            
            plt.figure(figsize=Config.GRAPH_FIGSIZE, dpi=Config.GRAPH_DPI)
            
            # Set dark theme
            bg_color = '#0E1117'
            grid_color = '#2E3440'
            text_color = '#FFFFFF'
            
            ax = plt.gca()
            ax.set_facecolor(bg_color)
            plt.gcf().patch.set_facecolor(bg_color)
            
            x_vals = np.linspace(xmin, xmax, 1000)
            
            for i, expr_string in enumerate(expressions):
                expr = self.parse_expression(expr_string)
                f = sp.lambdify(self.x_symbol, expr, 'numpy')
                
                try:
                    y_vals = f(x_vals)
                    y_vals = np.where(np.abs(y_vals) > 1e10, np.nan, y_vals)
                except:
                    y_vals = []
                    for x in x_vals:
                        try:
                            y = float(f(x))
                            if abs(y) > 1e10:
                                y = np.nan
                            y_vals.append(y)
                        except:
                            y_vals.append(np.nan)
                    y_vals = np.array(y_vals)
                
                color = colors[i % len(colors)]
                plt.plot(x_vals, y_vals, color=color, linewidth=2.5, 
                        label=f'f{i+1}(x) = {expr}')
            
            # Add grid and axes
            plt.grid(True, alpha=0.3, color=grid_color, linestyle='--')
            plt.axhline(y=0, color=text_color, linewidth=0.8, alpha=0.5)
            plt.axvline(x=0, color=text_color, linewidth=0.8, alpha=0.5)
            
            # Styling
            plt.xlabel('x', fontsize=12, color=text_color, fontweight='bold')
            plt.ylabel('f(x)', fontsize=12, color=text_color, fontweight='bold')
            plt.title('Multiple Functions', fontsize=14, color=text_color, 
                     fontweight='bold', pad=20)
            
            ax.spines['bottom'].set_color(text_color)
            ax.spines['top'].set_color(text_color)
            ax.spines['left'].set_color(text_color)
            ax.spines['right'].set_color(text_color)
            ax.tick_params(colors=text_color)
            
            legend = plt.legend(facecolor=bg_color, edgecolor=grid_color, 
                              fontsize=10, loc='best')
            plt.setp(legend.get_texts(), color=text_color)
            
            plt.xlim(xmin, xmax)
            
            # Save
            if filename is None:
                import hashlib
                filename = hashlib.md5('_'.join(expressions).encode()).hexdigest() + '.png'
            
            filepath = os.path.join(Config.GRAPH_DIR, filename)
            plt.tight_layout()
            plt.savefig(filepath, facecolor=bg_color, edgecolor='none', 
                       bbox_inches='tight', dpi=Config.GRAPH_DPI)
            plt.close()
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating multi-graph: {e}")
            raise

# Global graph generator instance
graph_gen = GraphGenerator()
