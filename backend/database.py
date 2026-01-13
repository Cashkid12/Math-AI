"""
Database module for MongoDB connection and operations
"""
from pymongo import MongoClient
from datetime import datetime
from config import Config
import logging
import uuid

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            if Config.MONGODB_URI:  # Only connect if URI is provided
                self.client = MongoClient(Config.MONGODB_URI)
                self.db = self.client[Config.DATABASE_NAME]
                self.problems = self.db.problems
                self.chats = self.db.chats  # New collection for chat history
                logger.info("Successfully connected to MongoDB")
                self.connected = True
            else:
                logger.warning("MONGODB_URI not provided, running without database")
                self.client = None
                self.db = None
                self.problems = None
                self.chats = None
                self.connected = False
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
            self.problems = None
            self.chats = None
            self.connected = False
    
    def save_chat_message(self, chat_id, role, content, metadata=None):
        """
        Save a chat message to database
        
        Args:
            chat_id: Unique identifier for the chat conversation
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata about the message
            
        Returns:
            Inserted document ID
        """
        if not self.connected:
            logger.warning("Database not connected, skipping save_chat_message")
            return None
        
        try:
            document = {
                'chat_id': chat_id,
                'role': role,
                'content': content,
                'metadata': metadata or {},
                'timestamp': datetime.utcnow()
            }
            result = self.chats.insert_one(document)
            logger.info(f"Saved chat message with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving chat message: {e}")
            return None
    
    def create_new_chat(self):
        """
        Create a new chat session
        
        Returns:
            Unique chat ID
        """
        if not self.connected:
            logger.warning("Database not connected, skipping create_new_chat")
            return str(uuid.uuid4())  # Return a chat ID but don't save to DB
        
        try:
            chat_id = str(uuid.uuid4())
            document = {
                'chat_id': chat_id,
                'created_at': datetime.utcnow(),
                'last_updated': datetime.utcnow()
            }
            result = self.chats.insert_one(document)
            logger.info(f"Created new chat session with ID: {chat_id}")
            return chat_id
        except Exception as e:
            logger.error(f"Error creating new chat: {e}")
            return None
    
    def get_chat_history(self, chat_id, limit=50):
        """
        Get chat history for a specific conversation
        
        Args:
            chat_id: Unique identifier for the chat conversation
            limit: Maximum number of messages to return
            
        Returns:
            List of chat messages
        """
        if not self.connected:
            logger.warning("Database not connected, returning empty chat history")
            return []
        
        try:
            messages = list(self.chats.find({
                'chat_id': chat_id,
                'role': {'$in': ['user', 'assistant']}  # Filter out session documents
            })
                          .sort('timestamp', 1)
                          .limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for message in messages:
                message['_id'] = str(message['_id'])
                message['timestamp'] = message['timestamp'].isoformat()
            
            return messages
        except Exception as e:
            logger.error(f"Error retrieving chat history: {e}")
            return []
    
    def get_all_chats(self, limit=20):
        """
        Get all chat sessions for a user
        
        Args:
            limit: Maximum number of chat sessions to return
            
        Returns:
            List of chat sessions
        """
        if not self.connected:
            logger.warning("Database not connected, returning empty chat list")
            return []
        
        try:
            # Find all documents that are chat sessions (not individual messages)
            chats = list(self.chats.find({
                'role': {'$exists': False}  # Chat session documents don't have role field
            })
                          .sort('created_at', -1)
                          .limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for chat in chats:
                chat['_id'] = str(chat['_id'])
                chat['created_at'] = chat['created_at'].isoformat()
                chat['last_updated'] = chat['last_updated'].isoformat()
            
            return chats
        except Exception as e:
            logger.error(f"Error retrieving chat sessions: {e}")
            return []
    
    def save_problem(self, problem_type, input_text, solution, steps, graph_url=None, chat_id=None):
        """
        Save a solved problem to database
        
        Args:
            problem_type: Type of problem (algebra, calculus, graph)
            input_text: Original problem input
            solution: Computed solution
            steps: List of solution steps
            graph_url: Optional URL to graph image
            chat_id: Optional chat session ID this problem belongs to
            
        Returns:
            Inserted document ID
        """
        if not self.connected:
            logger.warning("Database not connected, skipping save_problem")
            return None
        
        try:
            document = {
                'type': problem_type,
                'input': input_text,
                'solution': solution,
                'steps': steps,
                'graph_url': graph_url,
                'chat_id': chat_id,  # Link to chat session if provided
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
        if not self.connected:
            logger.warning("Database not connected, returning empty history")
            return []
        
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
        if not self.connected:
            logger.warning("Database not connected, returning default analytics")
            return {}
        
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
# Create a lazy-loading proxy to avoid startup errors when MongoDB is not configured
class DatabaseProxy:
    def __init__(self):
        self._instance = None
    
    def _get_instance(self):
        if self._instance is None:
            self._instance = Database()
        return self._instance
    
    def __getattr__(self, name):
        # Delegate all attribute access to the actual database instance
        return getattr(self._get_instance(), name)

# Create proxy instance
db = DatabaseProxy()