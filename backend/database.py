"""
Database module for MongoDB connection and operations
"""
from pymongo import MongoClient
from datetime import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.problems = self.db.problems
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def save_problem(self, problem_type, input_text, solution, steps, graph_url=None):
        """
        Save a solved problem to database
        
        Args:
            problem_type: Type of problem (algebra, calculus, graph)
            input_text: Original problem input
            solution: Computed solution
            steps: List of solution steps
            graph_url: Optional URL to graph image
            
        Returns:
            Inserted document ID
        """
        try:
            document = {
                'type': problem_type,
                'input': input_text,
                'solution': solution,
                'steps': steps,
                'graph_url': graph_url,
                'timestamp': datetime.utcnow()
            }
            result = self.problems.insert_one(document)
            logger.info(f"Saved problem with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving problem: {e}")
            return None
    
    def get_history(self, limit=20):
        """
        Get recent solved problems
        
        Args:
            limit: Maximum number of problems to return
            
        Returns:
            List of recent problems
        """
        try:
            problems = list(self.problems.find()
                          .sort('timestamp', -1)
                          .limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for problem in problems:
                problem['_id'] = str(problem['_id'])
                problem['timestamp'] = problem['timestamp'].isoformat()
            
            return problems
        except Exception as e:
            logger.error(f"Error retrieving history: {e}")
            return []
    
    def get_analytics(self):
        """
        Get usage analytics
        
        Returns:
            Dictionary with analytics data
        """
        try:
            total = self.problems.count_documents({})
            algebra_count = self.problems.count_documents({'type': 'algebra'})
            calculus_count = self.problems.count_documents({'type': 'calculus'})
            graph_count = self.problems.count_documents({'type': 'graph'})
            
            return {
                'total_problems': total,
                'algebra': algebra_count,
                'calculus': calculus_count,
                'graph': graph_count
            }
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")

# Global database instance
db = Database()
