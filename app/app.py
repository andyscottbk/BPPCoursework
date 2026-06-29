"""BPM Backend API - provides health and status endpoints."""
from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/health')
def health():
    """Health check endpoint for ALB target group."""
    return jsonify({
        'status': 'healthy',
        'service': 'bpm-frontend',
        'version': os.environ.get('APP_VERSION', '1.0.0')
    }), 200


@app.route('/api/status')
def status():
    """Application status endpoint consumed by React frontend."""
    return jsonify({
        'application': 'bpm-frontend',
        'status': 'operational',
        'environment': os.environ.get('APP_ENV', 'production')
    }), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
