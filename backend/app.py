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
from math_solver import solver
from graph_generator import graph_gen

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
                if '=' not in expr_to_graph:  # Not an equation, might be graphable
                    graph_path = graph_gen.generate_graph(expr_to_graph, -10, 10)
                    graph_filename = os.path.basename(graph_path)
                    result['graph_url'] = f"/api/graph/{graph_filename}"
            except:
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