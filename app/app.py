from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPM Application</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }
        .container { background: white; padding: 30px; border-radius: 8px; max-width: 600px; margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .status { color: #27ae60; font-weight: bold; }
        .endpoint { background: #ecf0f1; padding: 10px; border-radius: 4px; margin: 10px 0; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>BPM Frontend Application</h1>
        <p>Status: <span class="status">Running</span></p>
        <p>Environment: {{ env }}</p>
        <h2>Available Endpoints</h2>
        <div class="endpoint">GET /</div>
        <div class="endpoint">GET /health</div>
        <div class="endpoint">GET /api/status</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    env = os.environ.get('APP_ENV', 'production')
    return render_template_string(HTML_TEMPLATE, env=env)

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
    """Application status endpoint."""
    return jsonify({
        'application': 'bpm-frontend',
        'status': 'operational',
        'environment': os.environ.get('APP_ENV', 'production')
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
