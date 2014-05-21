from unittest import TestCase
from mock import patch, Mock

from yum_repo_client.repoclient import HttpClient

class HttpCallWithoutContextTests(TestCase):

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_get_without_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context=None)

        self.client.doHttpGet('/repo/querystuff')

        mock_connection.request.assert_called_with('GET', '/repo/querystuff', None, {'User-Agent': 'repoclient/1.0'})

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_delete_without_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context=None)

        self.client.doHttpDelete('/repo/deletestuff')

        mock_connection.request.assert_called_with('DELETE', '/repo/deletestuff', None, {'User-Agent': 'repoclient/1.0'})

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_post_without_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context=None)

        self.client.doHttpPost('/repo/mutatestuff')

        mock_connection.request.assert_called_with('POST', '/repo/mutatestuff', '', {'User-Agent': 'repoclient/1.0'})


class HttpCallWithContextTests(TestCase):

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_get_with_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context="/any/context")

        self.client.doHttpGet('/repo/querystuff')

        mock_connection.request.assert_called_with('GET', '/any/context/repo/querystuff', None, {'User-Agent': 'repoclient/1.0'})

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_delete_with_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context="/any/context")

        self.client.doHttpDelete('/repo/deletestuff')

        mock_connection.request.assert_called_with('DELETE', '/any/context/repo/deletestuff', None, {'User-Agent': 'repoclient/1.0'})

    @patch("yum_repo_client.repoclient.httplib")
    def test_should_post_with_context(self, http_lib):
        mock_connection = Mock()
        http_lib.HTTPConnection.return_value = mock_connection
        self.client = HttpClient("any-host.invalid", 42, context="/any/context")

        self.client.doHttpPost('/repo/mutatestuff')

        mock_connection.request.assert_called_with('POST', '/any/context/repo/mutatestuff', '', {'User-Agent': 'repoclient/1.0'})
