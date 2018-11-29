import pytest
from app import app

@pytest.fixture
def app():
	from app import app
	app.config['WTF_CSRF_ENABLED'] = False
	app.config['WTF_CSRF_METHODS'] = []
	return app
