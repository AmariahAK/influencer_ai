from flask import Flask, jsonify
from flask_cors import CORS
from routes.api import api_bp
from models.database import init_db
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # App configurations
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI', 'sqlite:///influencers.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max-limit
    )
    
    # Setup logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/influencer_ai.log', 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Influencer AI startup')
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

def main():
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

if __name__ == "__main__":
    main()
