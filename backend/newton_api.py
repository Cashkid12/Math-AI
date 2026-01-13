"""
Newton API Service for Equai AI
Handles communication with the Newton API for enhanced math problem solving
"""
import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

class NewtonAPI:
    """Service to interact with Newton API for mathematical operations"""
    
    def __init__(self):
        """Initialize Newton API service"""
        self.base_url = "https://newton.now.sh/api/v2"
        
    def _make_request(self, operation, expression):
        """
        Make a request to the Newton API
        
        Args:
            operation: The math operation to perform
            expression: The mathematical expression to operate on
            
        Returns:
            Dictionary with result from Newton API
        """
        try:
            # URL encode the expression
            encoded_expr = quote(expression, safe='')
            url = f"{self.base_url}/{operation}/{encoded_expr}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Newton API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error calling Newton API: {e}")
            return None
    
    def simplify(self, expression):
        """Simplify an expression"""
        return self._make_request('simplify', expression)
    
    def factor(self, expression):
        """Factor an expression"""
        return self._make_request('factor', expression)
    
    def derive(self, expression):
        """Find derivative of an expression"""
        return self._make_request('derive', expression)
    
    def integrate(self, expression):
        """Find integral of an expression"""
        return self._make_request('integrate', expression)
    
    def zeroes(self, expression):
        """Find zeros of an expression"""
        return self._make_request('zeroes', expression)
    
    def tangent(self, expression):
        """
        Find tangent line - expects format like '2|f(x)' where 2 is x value
        and f(x) is the function
        """
        return self._make_request('tangent', expression)
    
    def area(self, expression):
        """
        Find area under curve - expects format like '2:4|f(x)' where 2,4 are x values
        and f(x) is the function
        """
        return self._make_request('area', expression)
    
    def solve_equation(self, equation):
        """
        Solve an equation by converting to standard form and finding roots
        For equations like "x^2 + 2x = 3", convert to "x^2 + 2x - 3" and find zeroes
        """
        try:
            if '=' in equation:
                left, right = equation.split('=', 1)  # Split only on first occurrence
                # Move everything to left side: left - right = 0
                expr = f"({left.strip()})-({right.strip()})"
                return self.zeroes(expr)
            else:
                return self.zeroes(equation)
        except Exception as e:
            logger.error(f"Error solving equation: {e}")
            return None
    
    def expand(self, expression):
        """Expand an expression"""
        return self._make_request('expand', expression)
    
    def cosine(self, expression):
        """Cosine of an expression"""
        return self._make_request('cos', expression)
    
    def sine(self, expression):
        """Sine of an expression"""
        return self._make_request('sin', expression)
    
    def tangent(self, expression):
        """Tangent of an expression"""
        return self._make_request('tan', expression)
    
    def logarithm(self, expression):
        """Logarithm of an expression"""
        return self._make_request('log', expression)
    
    def absolute_value(self, expression):
        """Absolute value of an expression"""
        return self._make_request('abs', expression)
    
    def exponent(self, expression):
        """Exponential of an expression"""
        return self._make_request('exp', expression)
    
    def square_root(self, expression):
        """Square root of an expression"""
        return self._make_request('sqrt', expression)
    
    def get_operation_from_input(self, input_text):
        """
        Determine the appropriate operation based on the input text
        """
        input_lower = input_text.lower().strip()
        
        # Check for specific operation requests
        if any(word in input_lower for word in ['derive', 'derivative', 'd/dx', 'differentiat']):
            return 'derive'
        elif any(word in input_lower for word in ['integrate', 'integral', 'antideriv']):
            return 'integrate'
        elif any(word in input_lower for word in ['factor', 'factoring']):
            return 'factor'
        elif any(word in input_lower for word in ['simplify', 'simplified']):
            return 'simplify'
        elif any(word in input_lower for word in ['expand', 'expanded']):
            return 'expand'
        elif any(word in input_lower for word in ['solve', 'find x', 'x =']):
            return 'solve'
        elif any(word in input_lower for word in ['cos', 'cosine']):
            return 'cos'
        elif any(word in input_lower for word in ['sin', 'sine']):
            return 'sin'
        elif any(word in input_lower for word in ['tan', 'tangent']):
            return 'tan'
        elif any(word in input_lower for word in ['log', 'logarithm']):
            return 'log'
        elif any(word in input_lower for word in ['abs', 'absolute value']):
            return 'abs'
        elif any(word in input_lower for word in ['sqrt', 'square root']):
            return 'sqrt'
        elif any(word in input_lower for word in ['exp', 'exponent']):
            return 'exp'
        
        # Default to solve if it's an equation
        if '=' in input_text:
            return 'solve'
        
        # Default to simplify for expressions
        return 'simplify'
    
    def get_step_by_step_solution(self, operation, expression):
        """
        Get step-by-step solution by using multiple Newton API operations
        """
        try:
            steps = []
            explanations = []
            
            # Add original expression
            steps.append(f"📝 Original: {expression}")
            explanations.append("Starting with the given expression")
            
            # Clean the expression for specific operations
            clean_expr = expression
            if 'derive' in expression.lower():
                clean_expr = expression.lower().replace('derive ', '').replace('derivative ', '')
                operation = 'derive'
            elif 'integrate' in expression.lower():
                clean_expr = expression.lower().replace('integrate ', '').replace('integral ', '')
                operation = 'integrate'
            elif 'factor' in expression.lower():
                clean_expr = expression.lower().replace('factor ', '').replace('factoring ', '')
                operation = 'factor'
            
            # Perform the requested operation
            if operation == 'derive':
                result = self.derive(clean_expr)
                if result and 'result' in result:
                    steps.append(f"📈 Derivative: {result['result']}")
                    explanations.append("Found the derivative using differentiation rules")
                    return {
                        'steps': steps,
                        'explanations': explanations,
                        'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                        'solution': result['result']
                    }
            
            elif operation == 'integrate':
                result = self.integrate(clean_expr)
                if result and 'result' in result:
                    steps.append(f"🧮 Integral: {result['result']}")
                    explanations.append("Found the integral using integration rules")
                    return {
                        'steps': steps,
                        'explanations': explanations,
                        'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                        'solution': result['result']
                    }
            
            elif operation == 'factor':
                result = self.factor(clean_expr)
                if result and 'result' in result:
                    steps.append(f"🔢 Factored: {result['result']}")
                    explanations.append("Factored the expression into simpler components")
                    return {
                        'steps': steps,
                        'explanations': explanations,
                        'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                        'solution': result['result']
                    }
            
            elif '=' in expression:
                # Solve equation
                result = self.solve_equation(expression)
                if result and 'result' in result:
                    steps.append(f"✅ Solution: {result['result']}")
                    explanations.append("Solved the equation by finding values that satisfy it")
                    return {
                        'steps': steps,
                        'explanations': explanations,
                        'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                        'solution': result['result']
                    }
            else:
                # For general expressions, try to simplify
                result = self.simplify(clean_expr)
                if result and 'result' in result and result['result'] != clean_expr:
                    steps.append(f"✨ Simplified: {result['result']}")
                    explanations.append("Simplified by combining like terms and reducing")
                    return {
                        'steps': steps,
                        'explanations': explanations,
                        'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                        'solution': result['result']
                    }
            
            # If no specific operation was successful, return what we have
            return {
                'steps': steps,
                'explanations': explanations,
                'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                'solution': None
            }
        except Exception as e:
            logger.error(f"Error getting step-by-step solution: {e}")
            return {
                'steps': [f"Error: {str(e)}"],
                'explanations': ["Could not generate step-by-step solution"],
                'detailed_steps': [{'step': f"Error: {str(e)}", 'explanation': "Could not generate step-by-step solution"}],
                'solution': None
            }
    
    def _combine_steps_and_explanations(self, steps, explanations):
        """
        Combine steps and explanations into detailed output
        """
        detailed = []
        for i, step in enumerate(steps):
            if i < len(explanations):
                detailed.append({
                    'step': step,
                    'explanation': explanations[i]
                })
            else:
                detailed.append({
                    'step': step,
                    'explanation': ''
                })
        return detailed

# Global Newton API instance
newton_api = NewtonAPI()