"""Unit tests for BPM Flask API backend."""
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
    """Tests for the /health endpoint - critical for ALB routing."""

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


class TestStatusEndpoint:
    """Tests for the /api/status endpoint consumed by the React frontend."""

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

    def test_status_contains_application(self, client):
        """Status must identify the application."""
        response = client.get('/api/status')
        data = response.get_json()
        assert data['application'] == 'bpm-frontend'


class TestSecurityHeaders:
    """Security-focused tests relevant to MNPI handling."""

    def test_invalid_route_returns_404(self, client):
        """Unknown routes must return 404 - no stack trace exposure."""
        response = client.get('/mnpi/data')
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """POST to GET-only endpoints must return 405."""
        response = client.post('/health')
        assert response.status_code == 405

    def test_health_does_not_expose_env_vars(self, client):
        """Health endpoint must not leak environment variables."""
        response = client.get('/health')
        data = response.get_json()
        sensitive_keys = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'DB_PASSWORD']
        for key in sensitive_keys:
            assert key not in data

    def test_status_does_not_expose_secrets(self, client):
        """Status endpoint must not expose sensitive configuration."""
        response = client.get('/api/status')
        data = response.get_json()
        assert 'secret' not in str(data).lower()
        assert 'password' not in str(data).lower()
        assert 'key' not in str(data).lower()
