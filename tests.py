import pytest

class TestApp:
	def test_index_loads(self, client):
		response = client.get('/index')
		assert response.status_code == 200

