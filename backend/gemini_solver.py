"""
Gemini AI Integration for EquaAI
This module integrates Google's Gemini AI with the existing math solver
to create a hybrid system that can handle both mathematical and general questions.
"""
import google.generativeai as genai
import re
import logging
from newton_api import newton_api

logger = logging.getLogger(__name__)

# Configure Gemini API with the provided API key
genai.configure(api_key="AIzaSyC0Mm7OzHvW8B-vGGIe8_5ShDHxgcm8X0g")

class HybridSolver:
    def __init__(self):
        # Gemini is used for language understanding, Newton for mathematical computation
        pass
        # Use the correct model name for the current API
        # Try the most reliable models in order of preference
        model_names = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']
        
        self.gemini_model = None
        for model_name in model_names:
            try:
                self.gemini_model = genai.GenerativeModel(model_name)
                logger.info(f"Successfully initialized Gemini model: {model_name}")
                break
            except Exception as e:
                logger.warning(f"Could not initialize model {model_name}: {str(e)}")
                continue
        
        if self.gemini_model is None:
            raise Exception("Could not initialize any Gemini model. Please check your API key and model availability.")
        
    def solve_any(self, input_text):
        """
        Hybrid solver that uses both math solver and Gemini AI
        Following the required workflow:
        1. Send full user input to Gemini for language understanding
        2. Use Gemini for classification, extraction, translation, and reasoning
        3. Convert structured logic to valid math expressions
        4. Evaluate expressions using math evaluator
        5. Return step-by-step explanation and final answer
        
        Args:
            input_text: Any question as string (mathematical or general)
            
        Returns:
            Dictionary with solution, steps, explanations, and problem type
        """
        # Check if user wants specific type of output
        wants_steps = any(keyword in input_text.lower() for keyword in ['step', 'steps', 'show work', 'working', 'process', 'explain'])
        
        # First, check if this is a simple arithmetic expression that should be evaluated directly
        # Raw arithmetic expressions like '2+2', '5*3', '10/2' should be handled by Newton API
        arithmetic_pattern = r'^\s*[\d\s\+\-\*/\^\.\(\)]+\s*$'  # Simple arithmetic
        if re.match(arithmetic_pattern, input_text) and not any(c.isalpha() for c in input_text.replace('%', '').replace('π', '')):
            # This is a raw arithmetic expression, send to Newton API
            try:
                newton_result = newton_api.simplify(input_text)
                if newton_result and 'result' in newton_result:
                    solution = newton_result['result']
                    if not wants_steps:
                        return {
                            'solution': solution,
                            'problem_type': 'Arithmetic Expression',
                            'detailed_steps': [],
                            'steps': [],
                            'explanations': [],
                            'source': 'newton_api'
                        }
                    else:
                        step_result = newton_api.get_step_by_step_solution('simplify', input_text)
                        return {
                            'solution': solution,
                            'problem_type': 'Arithmetic Expression',
                            'detailed_steps': step_result.get('detailed_steps', []),
                            'steps': step_result.get('steps', []),
                            'explanations': step_result.get('explanations', []),
                            'source': 'newton_api'
                        }
                else:
                    # If Newton API doesn't return a result, return the input
                    return {
                        'solution': input_text,
                        'problem_type': 'Arithmetic Expression',
                        'detailed_steps': [],
                        'steps': [],
                        'explanations': ['Expression returned as-is'],
                        'source': 'newton_api'
                    }
            except Exception as e:
                logger.warning(f"Newton API failed for raw arithmetic '{input_text}': {str(e)}")
                return {
                    'solution': f"Error evaluating expression: {input_text}",
                    'problem_type': 'Evaluation Error',
                    'detailed_steps': [],
                    'steps': [],
                    'explanations': ['There was an issue evaluating this expression.'],
                    'source': 'error'
                }
        
        # For any text containing words or complex expressions, use Gemini for language understanding
        try:
            # Send full user input to Gemini for language understanding and reasoning only
            prompt = f"""
            You are EquaAI, an expert mathematical assistant. You are a language understanding and math reasoning engine.
            
            Analyze this user input: "{input_text}"
            
            You must return TWO separate outputs:
            
            A) EXPLANATION:
            - Provide a plain English explanation for the user
            - May include words and teaching-style reasoning
            - This will NOT be sent to the evaluator
            
            B) EXPRESSION:
            - Provide ONE single-line mathematical expression for evaluation
            - Must contain ONLY: digits (0-9), decimal points, and ASCII operators (+ - * / ( ))
            - NO words, NO symbols like × ÷ % $ ?, NO formatting or labels
            
            Format your response exactly as follows:
            EXPLANATION: [English explanation of the problem and solution approach]
            EXPRESSION: [clean ASCII mathematical expression]
            """
            
            response = self.gemini_model.generate_content(prompt)
            gemini_response = response.text.strip()
            
            # Parse Gemini's response to separate explanation from expression
            explanation = f"Solution for: {input_text}"
            expression = input_text  # Default fallback
            
            for line in gemini_response.split('\n'):
                if line.startswith('EXPLANATION:'):
                    explanation = line[12:].strip()
                elif line.startswith('EXPRESSION:'):
                    expression = line[11:].strip()
            
            # Validate that the expression contains only allowed characters
            # Only allow digits, decimal points, and basic operators
            valid_expression_pattern = r'^[0-9\+\-\*/\.\(\)\s]+$'
            if not re.match(valid_expression_pattern, expression):
                # If expression contains invalid characters, try to clean it
                # Remove common invalid characters but preserve the math
                cleaned_expression = re.sub(r'[×÷%$?]', '', expression)
                # Replace common alternatives with standard operators
                cleaned_expression = cleaned_expression.replace('−', '-')  # Unicode minus
                cleaned_expression = cleaned_expression.replace('×', '*')  # Unicode times
                cleaned_expression = cleaned_expression.replace('÷', '/')  # Unicode divide
                
                # Check again
                if re.match(valid_expression_pattern, cleaned_expression):
                    expression = cleaned_expression
                else:
                    # If still not valid, try to extract a basic math expression from the original
                    # Look for basic arithmetic patterns
                    basic_math_match = re.search(r'[0-9\+\-\*/\.\(\)]+[0-9\+\-\*/\.\(\)]', input_text)
                    if basic_math_match:
                        expression = basic_math_match.group()
                    else:
                        # As a last resort, try to process the original input
                        expression = input_text
            
            # Now send ONLY the clean expression to the math evaluator
            # Send ONLY the clean expression to the Newton API
            try:
                # Determine the appropriate operation for Newton API
                operation = newton_api.get_operation_from_input(expression)
                
                if operation == 'solve':
                    newton_result = newton_api.solve_equation(expression)
                elif operation == 'simplify':
                    newton_result = newton_api.simplify(expression)
                elif operation == 'factor':
                    newton_result = newton_api.factor(expression)
                elif operation == 'derive':
                    newton_result = newton_api.derive(expression)
                elif operation == 'integrate':
                    newton_result = newton_api.integrate(expression)
                elif operation == 'expand':
                    newton_result = newton_api.expand(expression)
                elif operation == 'sin':
                    newton_result = newton_api.sine(expression)
                elif operation == 'cos':
                    newton_result = newton_api.cosine(expression)
                elif operation == 'tan':
                    newton_result = newton_api.tangent(expression)
                elif operation == 'log':
                    newton_result = newton_api.logarithm(expression)
                elif operation == 'abs':
                    newton_result = newton_api.absolute_value(expression)
                elif operation == 'sqrt':
                    newton_result = newton_api.square_root(expression)
                elif operation == 'exp':
                    newton_result = newton_api.exponent(expression)
                else:
                    # Default to simplify
                    newton_result = newton_api.simplify(expression)
                
                if newton_result and 'result' in newton_result:
                    solution = newton_result['result']
                    
                    # Get step-by-step solution if requested
                    if wants_steps:
                        step_result = newton_api.get_step_by_step_solution(operation, expression)
                        
                        explanations = [explanation]
                        if step_result.get('explanations'):
                            explanations.extend(step_result['explanations'])
                        
                        detailed_steps = step_result.get('detailed_steps', [])
                        if not detailed_steps:
                            detailed_steps = [{'step': expression, 'explanation': explanation}]
                            
                        return {
                            'solution': solution,
                            'problem_type': f'Mathematical Expression ({operation})',
                            'detailed_steps': detailed_steps,
                            'steps': [expression],
                            'explanations': explanations,
                            'source': 'hybrid_gemini_newton'
                        }
                    else:
                        return {
                            'solution': solution,
                            'problem_type': f'Mathematical Expression ({operation})',
                            'detailed_steps': [],
                            'steps': [],
                            'explanations': [explanation],
                            'source': 'hybrid_gemini_newton'
                        }
                else:
                    # If Newton API doesn't return a result, return explanation only
                    return {
                        'solution': f"Unable to evaluate expression: {expression}",
                        'problem_type': 'Explanation Only',
                        'detailed_steps': [],
                        'steps': [],
                        'explanations': [explanation],
                        'source': 'gemini_explanation_only'
                    }
            except Exception as eval_error:
                logger.warning(f"Newton API failed to evaluate expression '{expression}': {str(eval_error)}")
                
                # If Newton API fails, return Gemini's explanation
                return {
                    'solution': f"Newton API unavailable for: {expression}",
                    'problem_type': 'Explanation Only',
                    'detailed_steps': [],
                    'steps': [],
                    'explanations': [explanation],
                    'source': 'gemini_explanation_only'
                }
            
        except Exception as e:
            logger.error(f"Gemini AI failed for '{input_text}': {str(e)}")
            
            # Fallback to Newton API if Gemini fails
            try:
                # Determine the appropriate operation for Newton API
                operation = newton_api.get_operation_from_input(input_text)
                
                if operation == 'solve':
                    newton_result = newton_api.solve_equation(input_text)
                elif operation == 'simplify':
                    newton_result = newton_api.simplify(input_text)
                elif operation == 'factor':
                    newton_result = newton_api.factor(input_text)
                elif operation == 'derive':
                    newton_result = newton_api.derive(input_text)
                elif operation == 'integrate':
                    newton_result = newton_api.integrate(input_text)
                elif operation == 'expand':
                    newton_result = newton_api.expand(input_text)
                elif operation == 'sin':
                    newton_result = newton_api.sine(input_text)
                elif operation == 'cos':
                    newton_result = newton_api.cosine(input_text)
                elif operation == 'tan':
                    newton_result = newton_api.tangent(input_text)
                elif operation == 'log':
                    newton_result = newton_api.logarithm(input_text)
                elif operation == 'abs':
                    newton_result = newton_api.absolute_value(input_text)
                elif operation == 'sqrt':
                    newton_result = newton_api.square_root(input_text)
                elif operation == 'exp':
                    newton_result = newton_api.exponent(input_text)
                else:
                    # Default to simplify
                    newton_result = newton_api.simplify(input_text)
                
                if newton_result and 'result' in newton_result:
                    solution = newton_result['result']
                    if not wants_steps:
                        return {
                            'solution': solution,
                            'problem_type': f'Mathematical Expression ({operation})',
                            'detailed_steps': [],
                            'steps': [],
                            'explanations': ['Processed directly by Newton API'],
                            'source': 'newton_api_fallback'
                        }
                    else:
                        step_result = newton_api.get_step_by_step_solution(operation, input_text)
                        return {
                            'solution': solution,
                            'problem_type': f'Mathematical Expression ({operation})',
                            'detailed_steps': step_result.get('detailed_steps', []),
                            'steps': step_result.get('steps', []),
                            'explanations': step_result.get('explanations', []) + ['Processed by Newton API'],
                            'source': 'newton_api_fallback'
                        }
                else:
                    # If both systems fail, return an appropriate error message
                    return {
                        'solution': f"I'm unable to process this question right now.",
                        'problem_type': 'Processing Error',
                        'detailed_steps': [],
                        'steps': [],
                        'explanations': ['Please try rephrasing your question'],
                        'source': 'error'
                    }
            except:
                # If both systems fail, return an appropriate error message
                return {
                    'solution': f"I'm unable to process this question right now.",
                    'problem_type': 'Processing Error',
                    'detailed_steps': [],
                    'steps': [],
                    'explanations': ['Please try rephrasing your question'],
                    'source': 'error'
                }

# Create a global instance
hybrid_solver = HybridSolver()