from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import routes
from routes.auth import auth_bp
from routes.captions import captions_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(captions_bp, url_prefix='/api')

# Health check route
@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'API is running'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)