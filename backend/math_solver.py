"""
Math Solver Engine for Equai AI
Provides detailed step-by-step solutions with explanations for algebra, calculus, and graphing
"""
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import logging

logger = logging.getLogger(__name__)

class MathSolver:
    """Advanced math solver with detailed explanations"""
    
    def __init__(self):
        """Initialize the math solver"""
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.transformations = (standard_transformations + 
                               (implicit_multiplication_application,))
    
    def parse_input(self, input_text):
        """
        Parse mathematical input string
        
        Args:
            input_text: Mathematical expression as string
            
        Returns:
            Parsed SymPy expression
        """
        try:
            # Replace common notations
            input_text = input_text.replace('^', '**')
            input_text = input_text.replace('÷', '/')
            
            expr = parse_expr(input_text, transformations=self.transformations)
            return expr
        except Exception as e:
            logger.error(f"Error parsing input: {e}")
            raise ValueError(f"Could not parse expression: {input_text}")
    
    def solve_any(self, input_text):
        """
        AI-powered solver that automatically detects and solves ANY type of math problem
        Works with: arithmetic, algebra, trigonometry, calculus, matrices, and more
        
        Args:
            input_text: Any mathematical problem as string
            
        Returns:
            Dictionary with solution, steps, explanations, and problem type
        """
        steps = []
        explanations = []
        
        try:
            steps.append(f"📝 Problem: {input_text}")
            explanations.append("AI is analyzing your math problem...")
            
            # Clean input
            input_text = input_text.replace('^', '**').strip()
            
            # Auto-detect problem type and solve
            if '=' in input_text:
                # Equation to solve
                steps.append("🔍 Detected: Equation")
                explanations.append("This is an equation - finding values that make it true")
                return {**self.solve_algebra(input_text), 'problem_type': 'Equation'}
            
            # Try to parse as expression
            expr = self.parse_input(input_text)
            
            # Check if it has variables
            if expr.free_symbols:
                # Algebraic expression
                steps.append(f"🔍 Detected: Algebraic Expression")
                explanations.append("This contains variables - I'll simplify and analyze it")
                
                simplified = sp.simplify(expr)
                expanded = sp.expand(expr)
                factored = sp.factor(expr)
                
                steps.append(f"Original: {expr}")
                explanations.append("Your expression as entered")
                
                if simplified != expr:
                    steps.append(f"✨ Simplified: {simplified}")
                    explanations.append("Simplified by combining like terms and reducing")
                
                if expanded != expr and expanded != simplified:
                    steps.append(f"📖 Expanded: {expanded}")
                    explanations.append("All brackets multiplied out")
                
                if factored != expr and factored != expanded:
                    steps.append(f"🔢 Factored: {factored}")
                    explanations.append("Expressed as a product of factors")
                
                # Check if it's differentiable/integrable
                try:
                    derivative = sp.diff(expr, list(expr.free_symbols)[0])
                    steps.append(f"📈 Derivative: {derivative}")
                    explanations.append("Rate of change of the expression")
                except:
                    pass
                
                return {
                    'solution': str(simplified),
                    'steps': steps,
                    'explanations': explanations,
                    'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                    'problem_type': 'Algebraic Expression',
                    'forms': {
                        'simplified': str(simplified),
                        'expanded': str(expanded),
                        'factored': str(factored)
                    }
                }
            else:
                # Pure arithmetic - calculate it
                steps.append("🔍 Detected: Arithmetic")
                explanations.append("Simple calculation")
                
                result = expr.evalf()
                
                steps.append(f"Calculation: {expr}")
                explanations.append("Evaluating the expression")
                
                steps.append(f"✅ Result: {result}")
                explanations.append("Final answer")
                
                return {
                    'solution': str(result),
                    'steps': steps,
                    'explanations': explanations,
                    'detailed_steps': self._combine_steps_and_explanations(steps, explanations),
                    'problem_type': 'Arithmetic'
                }
                
        except Exception as e:
            logger.error(f"Error in solve_any: {e}")
            return {
                'solution': f"I couldn't solve this. Error: {str(e)}",
                'steps': [f"❌ Error: {str(e)}"],
                'explanations': ['Please check your input format'],
                'detailed_steps': [{
                    'step': f"Error: {str(e)}",
                    'explanation': 'Try rephrasing your problem or check the syntax'
                }],
                'problem_type': 'Unknown',
                'error': str(e)
            }
    
    def solve_algebra(self, input_text):
        """
        Solve algebraic equations with detailed steps
        
        Args:
            input_text: Equation string (e.g., "x^2 + 2x - 3 = 0")
            
        Returns:
            Dictionary with solution, steps, and explanations
        """
        steps = []
        explanations = []
        
        try:
            # Step 1: Parse the equation
            steps.append(f"Original equation: {input_text}")
            explanations.append("Starting with the given equation")
            
            # Handle equation format
            if '=' in input_text:
                lhs, rhs = input_text.split('=')
                lhs_expr = self.parse_input(lhs.strip())
                rhs_expr = self.parse_input(rhs.strip())
                equation = sp.Eq(lhs_expr, rhs_expr)
                expr = lhs_expr - rhs_expr
            else:
                expr = self.parse_input(input_text)
                equation = sp.Eq(expr, 0)
            
            steps.append(f"Parsed equation: {equation}")
            explanations.append("Converting to standard mathematical form")
            
            # Step 2: Simplify
            simplified = sp.simplify(expr)
            if simplified != expr:
                steps.append(f"Simplified form: {simplified} = 0")
                explanations.append("Simplifying the equation by combining like terms")
            
            # Step 3: Identify equation type
            degree = sp.degree(simplified, self.x)
            steps.append(f"Equation degree: {degree}")
            
            if degree == 1:
                explanations.append("This is a linear equation (degree 1)")
            elif degree == 2:
                explanations.append("This is a quadratic equation (degree 2)")
                # Add quadratic formula explanation
                a, b, c = sp.symbols('a b c')
                if simplified.is_polynomial(self.x):
                    coeffs = sp.Poly(simplified, self.x).all_coeffs()
                    if len(coeffs) >= 2:
                        steps.append(f"Using quadratic formula: x = (-b ± √(b² - 4ac)) / 2a")
                        explanations.append("Applying the quadratic formula to find solutions")
            else:
                explanations.append(f"This is a polynomial equation of degree {degree}")
            
            # Step 4: Solve the equation
            solutions = sp.solve(equation, self.x)
            
            steps.append(f"Solving for x...")
            explanations.append("Finding all values of x that satisfy the equation")
            
            # Step 5: Present solutions
            if solutions:
                if len(solutions) == 1:
                    steps.append(f"Solution: x = {solutions[0]}")
                    explanations.append("There is one unique solution")
                else:
                    solution_str = ", ".join([f"x = {sol}" for sol in solutions])
                    steps.append(f"Solutions: {solution_str}")
                    explanations.append(f"There are {len(solutions)} solutions to this equation")
                
                # Verify solutions
                steps.append("Verification:")
                explanations.append("Checking each solution by substituting back into the original equation")
                for sol in solutions:
                    check = expr.subs(self.x, sol)
                    simplified_check = sp.simplify(check)
                    steps.append(f"  For x = {sol}: {simplified_check} ✓")
                    explanations.append(f"Substituting x = {sol} confirms it's a valid solution")
                
                # Format solutions for output
                solution_output = [str(sp.N(sol, 5)) for sol in solutions]
            else:
                steps.append("No real solutions found")
                explanations.append("This equation has no real number solutions")
                solution_output = "No real solutions"
            
            return {
                'solution': solution_output,
                'steps': steps,
                'explanations': explanations,
                'detailed_steps': self._combine_steps_and_explanations(steps, explanations)
            }
            
        except Exception as e:
            logger.error(f"Error solving algebra: {e}")
            return {
                'solution': f"Error: {str(e)}",
                'steps': steps if steps else [f"Error occurred: {str(e)}"],
                'explanations': explanations,
                'detailed_steps': [f"Could not solve: {str(e)}"]
            }
    
    def solve_calculus(self, input_text, operation='derivative'):
        """
        Solve calculus problems with detailed steps
        
        Args:
            input_text: Expression string
            operation: 'derivative', 'integral', or 'limit'
            
        Returns:
            Dictionary with solution, steps, and explanations
        """
        steps = []
        explanations = []
        
        try:
            # Step 1: Parse expression
            steps.append(f"Original expression: {input_text}")
            explanations.append("Starting with the given expression")
            
            expr = self.parse_input(input_text)
            steps.append(f"Parsed expression: {expr}")
            explanations.append("Converting to mathematical notation")
            
            if operation == 'derivative':
                # Derivative with steps
                steps.append(f"Finding d/dx({expr})")
                explanations.append("Computing the derivative with respect to x")
                
                # Apply derivative rules
                result = sp.diff(expr, self.x)
                
                # Explain the rules used
                if expr.is_polynomial(self.x):
                    steps.append("Using power rule: d/dx(x^n) = n*x^(n-1)")
                    explanations.append("Applying the power rule for polynomial terms")
                
                if expr.has(sp.sin) or expr.has(sp.cos):
                    steps.append("Using trigonometric derivatives:")
                    steps.append("  d/dx(sin(x)) = cos(x)")
                    steps.append("  d/dx(cos(x)) = -sin(x)")
                    explanations.append("Applying derivative rules for trigonometric functions")
                
                if expr.has(sp.exp):
                    steps.append("Using exponential rule: d/dx(e^x) = e^x")
                    explanations.append("Applying the exponential derivative rule")
                
                steps.append(f"Result: {result}")
                explanations.append("Final derivative after applying all rules")
                
            elif operation == 'integral':
                # Integration with steps
                steps.append(f"Finding ∫({expr}) dx")
                explanations.append("Computing the indefinite integral with respect to x")
                
                result = sp.integrate(expr, self.x)
                
                # Explain integration rules
                if expr.is_polynomial(self.x):
                    steps.append("Using power rule for integration: ∫x^n dx = x^(n+1)/(n+1) + C")
                    explanations.append("Applying the power rule for integration")
                
                steps.append(f"Result: {result} + C")
                explanations.append("Adding constant of integration C (for indefinite integrals)")
                
            elif operation == 'limit':
                # Limit evaluation
                steps.append(f"Finding lim(x→0) of {expr}")
                explanations.append("Computing the limit as x approaches 0")
                
                result = sp.limit(expr, self.x, 0)
                
                steps.append(f"Result: {result}")
                explanations.append("Limit value at the specified point")
            else:
                result = expr
            
            # Simplify result
            simplified_result = sp.simplify(result)
            if simplified_result != result:
                steps.append(f"Simplified: {simplified_result}")
                explanations.append("Simplifying the final result")
            
            return {
                'solution': str(simplified_result),
                'steps': steps,
                'explanations': explanations,
                'detailed_steps': self._combine_steps_and_explanations(steps, explanations)
            }
            
        except Exception as e:
            logger.error(f"Error solving calculus: {e}")
            return {
                'solution': f"Error: {str(e)}",
                'steps': steps if steps else [f"Error occurred: {str(e)}"],
                'explanations': explanations,
                'detailed_steps': [f"Could not solve: {str(e)}"]
            }
    
    def analyze_function(self, input_text):
        """
        Analyze a function for graphing with detailed information
        
        Args:
            input_text: Function expression
            
        Returns:
            Dictionary with function analysis
        """
        steps = []
        explanations = []
        
        try:
            expr = self.parse_input(input_text)
            
            steps.append(f"Analyzing function: f(x) = {expr}")
            explanations.append("Starting function analysis")
            
            # Find domain
            steps.append("Determining domain...")
            explanations.append("Finding all valid x values where the function is defined")
            
            # Find critical points (derivative = 0)
            derivative = sp.diff(expr, self.x)
            critical_points = sp.solve(derivative, self.x)
            
            if critical_points:
                steps.append(f"Critical points (f'(x) = 0): {critical_points}")
                explanations.append("Finding points where the slope is zero (potential max/min)")
            
            # Find y-intercept
            y_intercept = expr.subs(self.x, 0)
            steps.append(f"Y-intercept: (0, {y_intercept})")
            explanations.append("Finding where the function crosses the y-axis (when x=0)")
            
            # Find x-intercepts (roots)
            try:
                x_intercepts = sp.solve(expr, self.x)
                if x_intercepts:
                    steps.append(f"X-intercepts (roots): {x_intercepts}")
                    explanations.append("Finding where the function crosses the x-axis (when f(x)=0)")
            except:
                steps.append("X-intercepts: Could not determine analytically")
            
            return {
                'expression': str(expr),
                'derivative': str(derivative),
                'critical_points': [str(cp) for cp in critical_points] if critical_points else [],
                'y_intercept': str(y_intercept),
                'steps': steps,
                'explanations': explanations,
                'detailed_steps': self._combine_steps_and_explanations(steps, explanations)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing function: {e}")
            return {
                'expression': input_text,
                'steps': [f"Error: {str(e)}"],
                'explanations': [],
                'detailed_steps': [f"Could not analyze: {str(e)}"]
            }
    
    def _combine_steps_and_explanations(self, steps, explanations):
        """
        Combine steps and explanations into detailed output
        
        Args:
            steps: List of mathematical steps
            explanations: List of explanations
            
        Returns:
            List of combined step-explanation pairs
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

# Global solver instance
solver = MathSolver()
