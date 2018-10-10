import pytest


class TestApp:

	def test_index_loads(self, client):
		response = client.get(url_for('index'))
		assert response.status_code == 200

