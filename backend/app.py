"""
Equai AI - Flask Backend API
Main application file with all routes and endpoints
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import os
from config import Config
from database import db
# Import solver with fallback
try:
    from gemini_solver import hybrid_solver as solver
    print("Successfully loaded Gemini-based solver")
except ImportError as e:
    print(f"Failed to load gemini_solver: {e}")
    # Fallback to math_solver only
    from math_solver import MathSolver
    
    class FallbackSolver:
        def solve_any(self, input_text):
            math_solver = MathSolver()
            return math_solver.solve_any(input_text)
    
    solver = FallbackSolver()
    print("Using fallback math-only solver")
except Exception as e:
    print(f"Unexpected error loading solver: {e}")
    # Fallback to math_solver only
    from math_solver import MathSolver
    
    class FallbackSolver:
        def solve_any(self, input_text):
            math_solver = MathSolver()
            return math_solver.solve_any(input_text)
    
    solver = FallbackSolver()
    print("Using fallback math-only solver")

# Import graph generator with fallback
try:
    from graph_generator import graph_gen
    print("Successfully loaded graph generator")
except ImportError as e:
    print(f"Failed to load graph_generator: {e}")
    
    class FallbackGraphGen:
        def generate_graph(self, expression, xmin, xmax):
            # Create a placeholder graph
            import matplotlib.pyplot as plt
            import numpy as np
            import os
            import uuid
            
            # Create a simple graph with just axes
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot([xmin, xmax], [0, 0], 'k-', linewidth=0.5)  # x-axis
            ax.plot([0, 0], [xmin/2, xmax/2], 'k-', linewidth=0.5)  # y-axis
            ax.grid(True, alpha=0.3)
            ax.set_title(f"Graph of: {expression}")
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            
            # Create static directory if it doesn't exist
            if not os.path.exists('static'):
                os.makedirs('static')
            if not os.path.exists('static/graphs'):
                os.makedirs('static/graphs')
            
            # Generate unique filename
            filename = f"graph_{uuid.uuid4().hex}.png"
            filepath = os.path.join('static/graphs', filename)
            
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            return filepath
        
        def generate_multi_graph(self, expressions, xmin, xmax):
            return self.generate_graph('multiple', xmin, xmax)
    
    graph_gen = FallbackGraphGen()
    print("Using fallback graph generator")
except Exception as e:
    print(f"Unexpected error loading graph generator: {e}")
    
    class FallbackGraphGen:
        def generate_graph(self, expression, xmin, xmax):
            import matplotlib.pyplot as plt
            import os
            import uuid
            
            # Create a simple graph with just axes
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f"Graph not available:\n{expression}", 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, fontsize=12)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_title(f"Graph of: {expression}")
            
            # Create static directory if it doesn't exist
            if not os.path.exists('static'):
                os.makedirs('static')
            if not os.path.exists('static/graphs'):
                os.makedirs('static/graphs')
            
            # Generate unique filename
            filename = f"graph_{uuid.uuid4().hex}.png"
            filepath = os.path.join('static/graphs', filename)
            
            plt.savefig(filepath, dpi=100, bbox_inches='tight')
            plt.close()
            
            return filepath
        
        def generate_multi_graph(self, expressions, xmin, xmax):
            return self.generate_graph('multiple', xmin, xmax)
    
    graph_gen = FallbackGraphGen()
    print("Using fallback graph generator")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Create static directory for graphs
if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists('static/graphs'):
    os.makedirs('static/graphs')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Equai AI Backend',
        'version': '1.0.0'
    })

@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """
    AI-powered math problem solver - handles ANY type of math automatically
    
    Expected JSON input:
    {
        "input": "any mathematical problem or question"
    }
    
    Returns:
    {
        "solution": "result",
        "steps": ["step1", "step2", ...],
        "explanations": ["explanation1", "explanation2", ...],
        "detailed_steps": [{"step": "...", "explanation": "..."}, ...],
        "problem_type": "detected type",
        "graph_url": "/api/graph?expr=..." (if applicable)
    }
    """
    try:
        data = request.json
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input'
            }), 400
        
        input_text = data['input'].strip()
        
        if not input_text:
            return jsonify({
                'error': 'Input cannot be empty'
            }), 400
        
        logger.info(f"AI Solving: {input_text}")
        
        # Let AI detect the problem type and solve
        result = solver.solve_any(input_text)
        
        # Try to generate graph if it's a function
        if result.get('solution') and not result.get('error'):
            try:
                # Check if solution contains a function we can graph
                expr_to_graph = result.get('solution', input_text)
                if '=' not in str(expr_to_graph):  # Not an equation, might be graphable
                    graph_path = graph_gen.generate_graph(str(expr_to_graph), -10, 10)
                    graph_filename = os.path.basename(graph_path)
                    result['graph_url'] = f"/api/graph/{graph_filename}"
            except Exception as e:
                logger.error(f"Error generating graph: {e}")
                pass  # No graph needed
        
        # Save to database
        try:
            db.save_problem(
                problem_type=result.get('problem_type', 'auto'),
                input_text=input_text,
                solution=str(result.get('solution', '')),
                steps=result.get('steps', []),
                graph_url=result.get('graph_url')
            )
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
        
        return jsonify(result), 200
        
    except ValueError as e:
        logger.error(f"ValueError in solve: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error in solve endpoint: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/<filename>', methods=['GET'])
def get_graph(filename):
    """
    Serve generated graph images
    
    Args:
        filename: Name of the graph file
        
    Returns:
        PNG image file
    """
    try:
        filepath = os.path.join(Config.GRAPH_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')
        else:
            return jsonify({'error': 'Graph not found'}), 404
    except Exception as e:
        logger.error(f"Error serving graph: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/graph', methods=['GET'])
def generate_graph_url():
    """
    Generate a graph from URL parameters
    
    Query parameters:
        expr: Mathematical expression
        xmin: Minimum x value (default: -10)
        xmax: Maximum x value (default: 10)
        
    Returns:
        PNG image file
    """
    try:
        expr = request.args.get('expr')
        if not expr:
            return jsonify({'error': 'Missing expr parameter'}), 400
        
        xmin = float(request.args.get('xmin', -10))
        xmax = float(request.args.get('xmax', 10))
        
        # Generate graph
        graph_path = graph_gen.generate_graph(expr, xmin, xmax)
        
        return send_file(graph_path, mimetype='image/png')
        
    except ValueError as e:
        logger.error(f"ValueError in graph generation: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating graph: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/new', methods=['POST'])
def create_chat():
    """
    Create a new chat session
    
    Returns:
        JSON with new chat ID
    """
    try:
        chat_id = db.create_new_chat()
        if chat_id:
            return jsonify({
                'chat_id': chat_id,
                'status': 'success'
            }), 200
        else:
            return jsonify({'error': 'Failed to create chat session'}), 500
    except Exception as e:
        logger.error(f"Error creating chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/<chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    """
    Get messages for a specific chat
    
    Args:
        chat_id: Unique chat identifier
        
    Returns:
        JSON list of messages
    """
    try:
        messages = db.get_chat_history(chat_id)
        return jsonify({
            'chat_id': chat_id,
            'messages': messages,
            'count': len(messages)
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving chat messages: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chats', methods=['GET'])
def get_chats():
    """
    Get all chat sessions
    
    Query parameters:
        limit: Maximum number of results (default: 20)
        
    Returns:
        JSON list of chat sessions
    """
    try:
        limit = int(request.args.get('limit', 20))
        chats = db.get_all_chats(limit)
        
        return jsonify({
            'chats': chats,
            'count': len(chats)
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving chats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat_with_equai():
    """
    Chat with EquaAI - handles both math and general questions
    
    Expected JSON input:
    {
        "message": "user message",
        "chat_id": "optional chat session ID (creates new if not provided)"
    }
    
    Returns:
    {
        "response": "AI response",
        "chat_id": "chat session ID",
        "source": "math_solver or gemini_ai",
        "graph_url": "optional graph URL for math problems"
    }
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400
        
        user_message = data['message'].strip()
        chat_id = data.get('chat_id')
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400
        
        # Create new chat if no chat_id provided
        if not chat_id:
            chat_id = db.create_new_chat()
            if not chat_id:
                return jsonify({'error': 'Failed to create chat session'}), 500
        
        # Save user message
        db.save_chat_message(chat_id, 'user', user_message)
        
        logger.info(f"Chat with EquaAI: {user_message}")
        
        # Let the hybrid solver handle the message
        result = solver.solve_any(user_message)
        
        ai_response = result.get('solution', 'I couldn\'t process your request')
        
        # Save AI response
        db.save_chat_message(chat_id, 'assistant', ai_response, {
            'source': result.get('source', 'unknown'),
            'problem_type': result.get('problem_type')
        })
        
        # Try to generate graph if it's a math problem
        graph_url = None
        if result.get('source') == 'math_solver' and result.get('problem_type', '').lower() != 'general question':
            try:
                expr_to_graph = result.get('solution', user_message)
                # Only try to graph simple expressions that don't contain alphabetic variables
                expr_str = str(expr_to_graph)
                if '=' not in expr_str and all(not c.isalpha() or c in ['x', 'y', 'z'] for c in expr_str):
                    # Simple expression, try to graph it
                    graph_path = graph_gen.generate_graph(expr_str, -10, 10)
                    graph_filename = os.path.basename(graph_path)
                    graph_url = f"/api/graph/{graph_filename}"
            except Exception as e:
                logger.error(f"Error generating graph: {e}")
                pass  # No graph needed
        
        # Save to database as a problem if it's a math question
        if result.get('source') == 'math_solver':
            try:
                db.save_problem(
                    problem_type=result.get('problem_type', 'math'),
                    input_text=user_message,
                    solution=str(result.get('solution', '')),
                    steps=result.get('steps', []),
                    graph_url=graph_url,
                    chat_id=chat_id
                )
            except Exception as e:
                logger.error(f"Error saving to database: {e}")
        
        response_data = {
            'response': ai_response,
            'chat_id': chat_id,
            'source': result.get('source', 'unknown'),
            'problem_type': result.get('problem_type')
        }
        
        if graph_url:
            response_data['graph_url'] = graph_url
        
        return jsonify(response_data), 200
        
    except ValueError as e:
        logger.error(f"ValueError in chat: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get recent problem-solving history
    
    Query parameters:
        limit: Maximum number of results (default: 20)
        
    Returns:
        List of recent problems with solutions
    """
    try:
        limit = int(request.args.get('limit', 20))
        history = db.get_history(limit)
        
        return jsonify({
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Get usage analytics
    
    Returns:
        Analytics data including problem counts by type
    """
    try:
        analytics = db.get_analytics()
        return jsonify(analytics), 200
    except Exception as e:
        logger.error(f"Error retrieving analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/multi-graph', methods=['POST'])
def generate_multi_graph():
    """
    Generate graph with multiple functions
    
    Expected JSON input:
    {
        "expressions": ["expr1", "expr2", ...],
        "xmin": -10,
        "xmax": 10
    }
    
    Returns:
        Graph URL
    """
    try:
        data = request.json
        expressions = data.get('expressions', [])
        
        if not expressions:
            return jsonify({'error': 'Missing expressions'}), 400
        
        xmin = float(data.get('xmin', -10))
        xmax = float(data.get('xmax', 10))
        
        graph_path = graph_gen.generate_multi_graph(expressions, xmin, xmax)
        graph_filename = os.path.basename(graph_path)
        
        return jsonify({
            'graph_url': f"/api/graph/{graph_filename}"
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating multi-graph: {e}")
        return jsonify({'error': str(e)}), 500

# Serve React frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve React frontend static files in production"""
    if path != "" and os.path.exists(f"static/{path}"):
        return send_file(f"static/{path}")
    elif path == "" or path.endswith(".html") or "." not in path:
        return send_file("static/index.html")
    else:
        return send_file("static/index.html")

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Equai AI Backend Server...")
    logger.info(f"Server running on http://localhost:{Config.PORT}")
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )