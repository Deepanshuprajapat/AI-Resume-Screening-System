import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"})

    from routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
