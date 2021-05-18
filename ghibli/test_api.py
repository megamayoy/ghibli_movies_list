from django.test import TestCase
from ghibli.api import GhibliAPI
from unittest.mock import patch
from requests.exceptions import RequestException, ConnectionError

class GhibliAPITest(TestCase):
    def setUp(self):
        self.ghibli_api_obj = GhibliAPI()
        self.people_api_url = (
            'https://ghibliapi.herokuapp.com/people/'
        )
        self.films_api_url = (
            'https://ghibliapi.herokuapp.com/films/'
        )

    @patch("requests.get")
    def test_request_is_sent_with_correct_url(self, request_mock):
        self.ghibli_api_obj.get_resource("films")
        request_mock.assert_called_with(self.films_api_url)

        expected_url = self.films_api_url + "?fields=id,title"
        self.ghibli_api_obj.get_resource("films", fields=["id","title"])
        request_mock.assert_called_with(expected_url)

        self.ghibli_api_obj.get_resource("people")
        request_mock.assert_called_with(self.people_api_url)

        expected_url = self.people_api_url + "?fields=id"
        self.ghibli_api_obj.get_resource("people", fields=["id"])
        request_mock.assert_called_with(expected_url)

    @patch("requests.get",side_effect=[RequestException, ConnectionError])
    def test_api_returns_empty_content_when_exceptions_occur(
        self, request_mock
    ):
        # when request excpetion occurs
        content = self.ghibli_api_obj.get_resource("people")
        self.assertEqual(content, {})

        # when connection error occurs
        content = self.ghibli_api_obj.get_resource("films")
        self.assertEqual(content, {})



