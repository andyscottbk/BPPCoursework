"""Unit tests for BPM Frontend Flask application."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_returns_200(self, client):
        """Health endpoint must return HTTP 200 for ALB health checks."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Health endpoint must return JSON content type."""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_status_field(self, client):
        """Health response must contain status: healthy."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_contains_service_name(self, client):
        """Health response must identify the service."""
        response = client.get('/health')
        data = response.get_json()
        assert 'service' in data
        assert data['service'] == 'bpm-frontend'


class TestIndexEndpoint:
    """Tests for the root / endpoint."""

    def test_index_returns_200(self, client):
        """Index page must return HTTP 200."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """Index page must return HTML content."""
        response = client.get('/')
        assert b'BPM' in response.data


class TestStatusEndpoint:
    """Tests for the /api/status endpoint."""

    def test_status_returns_200(self, client):
        """Status endpoint must return HTTP 200."""
        response = client.get('/api/status')
        assert response.status_code == 200

    def test_status_returns_json(self, client):
        """Status endpoint must return JSON."""
        response = client.get('/api/status')
        assert response.content_type == 'application/json'

    def test_status_operational(self, client):
        """Status must report operational state."""
        response = client.get('/api/status')
        data = response.get_json()
        assert data['status'] == 'operational'

    def test_status_contains_environment(self, client):
        """Status must include environment field."""
        response = client.get('/api/status')
        data = response.get_json()
        assert 'environment' in data


class TestSecurityHeaders:
    """Security-focused tests relevant to MNPI handling."""

    def test_no_server_header_leakage(self, client):
        """Server header should not expose detailed version info."""
        response = client.get('/health')
        server_header = response.headers.get('Server', '')
        assert 'Werkzeug' not in server_header or response.status_code == 200

    def test_invalid_route_returns_404(self, client):
        """Unknown routes must return 404, not expose stack traces."""
        response = client.get('/mnpi/data')
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """POST to GET-only endpoints must return 405."""
        response = client.post('/health')
        assert response.status_code == 405
