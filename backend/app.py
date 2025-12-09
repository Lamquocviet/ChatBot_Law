"""
Flask API server for RAG Chatbot
Provides REST API endpoints for frontend communication
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processing import RAG
import threading
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_DIR), 'frontend')

# Initialize Flask app with static folder config
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)  # Enable CORS for frontend requests

# Initialize RAG system
rag_instance = None
initialization_done = False
initialization_error = None


def initialize_rag():
    """Initialize RAG system on first request"""
    global rag_instance, initialization_done, initialization_error
    
    if initialization_done:
        return rag_instance
    
    try:
        logger.info("Initializing RAG system...")
        rag_instance = RAG()
        # Do NOT automatically re-index on startup (very slow).
        # Indexing should be triggered manually via /api/index or by setting
        # environment variable FORCE_INDEX=true for dev workflows.
        if os.getenv('FORCE_INDEX', 'false').lower() == 'true':
            logger.info("FORCE_INDEX enabled — creating Vector DB now...")
            rag_instance.create_vectordb()

        initialization_done = True
        logger.info("RAG system initialized (indexing skipped by default).")
        return rag_instance
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        initialization_error = str(e)
        return None


@app.route('/', methods=['GET'])
def serve_index():
    """Serve index.html as the root"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory(FRONTEND_DIR, filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'rag_initialized': initialization_done,
        'error': initialization_error
    })


@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize RAG system"""
    global initialization_done, initialization_error
    
    if initialization_done:
        return jsonify({
            'status': 'success',
            'message': 'RAG system already initialized'
        })
    
    rag = initialize_rag()
    
    if rag is None:
        return jsonify({
            'status': 'error',
            'message': 'Failed to initialize RAG system',
            'error': initialization_error
        }), 500
    
    return jsonify({
        'status': 'success',
        'message': 'RAG system initialized successfully'
    })


@app.route('/api/index', methods=['POST'])
def trigger_index():
    """Trigger vector DB creation (indexing) in background."""
    global initialization_done

    if not initialization_done:
        return jsonify({'status': 'error', 'message': 'RAG not initialized'}), 503

    def _run_index():
        try:
            logger.info('Background indexing started')
            rag_instance.create_vectordb()
            logger.info('Background indexing finished')
        except Exception as e:
            logger.error(f'Indexing error: {e}')

    thread = threading.Thread(target=_run_index, daemon=True)
    thread.start()

    return jsonify({'status': 'accepted', 'message': 'Indexing started in background'})


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Expected JSON: {
        "question": "user question here"
    }
    """
    try:
        # Initialize RAG if not already done
        if not initialization_done:
            rag = initialize_rag()
            if rag is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to initialize RAG system',
                    'error': initialization_error
                }), 500
        
        # Get request data
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing "question" field in request'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Question cannot be empty'
            }), 400
        
        logger.info(f"Processing question: {question}")
        
        # Generate response using RAG
        response = rag_instance.generate_response(question)
        
        return jsonify({
            'status': 'success',
            'question': question,
            'answer': response,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error processing request',
            'error': str(e)
        }), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """
    Streaming chat endpoint (for future use)
    Allows real-time streaming of responses
    """
    try:
        # Initialize RAG if not already done
        if not initialization_done:
            rag = initialize_rag()
            if rag is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to initialize RAG system'
                }), 500
        
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing "question" field in request'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Question cannot be empty'
            }), 400
        
        # Generate response
        response = rag_instance.generate_response(question)
        
        return jsonify({
            'status': 'success',
            'question': question,
            'answer': response
        })
    
    except Exception as e:
        logger.error(f"Error in streaming endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error processing request',
            'error': str(e)
        }), 500


@app.route('/api/articles/<int:article_number>', methods=['GET'])
def get_article(article_number):
    """Get specific article from law"""
    try:
        if not initialization_done:
            return jsonify({
                'status': 'error',
                'message': 'RAG system not initialized'
            }), 503
        
        query = f"Điều {article_number}"
        response = rag_instance.search_raw_article(query)
        
        if response:
            return jsonify({
                'status': 'success',
                'article': article_number,
                'content': response
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Article {article_number} not found'
            }), 404
    
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error fetching article',
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(e)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
