from unittest.mock import MagicMock, patch
from django.test import TestCase
from rest_framework import status
from films.views import FilmsList
from rest_framework.request import Request, HttpRequest

class FilmsListingAPI(TestCase):

    def setUp(self):
        self.api_class = FilmsList
        self.url = "/movies/"
        self.films_sample = [
            {
                "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
                "title": "Castle in the Sky"
            },
            {
                "id": "12cfb892-aac0-4c5b-94af-521852e46d6a",
                "title": "Grave of the Fireflies"
            }
        ]
        self.actors_sample = [
                {
                    "name": "Pazu",
                    "films": [
                    "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                    ]
                },
                {
                    "name": "Lusheeta Toel Ul Laputa",
                    "films": [
                    "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                    ]
                }
        ]
        self.output_sample = [
            {
                'title': 'You got mail',
                'actors': ['Tom Hanks', 'Meg Ryan']
            },
            {
                 'title': 'Twilight',
                 'actors': ["kristen stewart"]
            }
        ]

    def test_correct_output_format_of_films_and_actors(self):
        expected_output = [
            {
                'title': 'Castle in the Sky',
                'actors': ['Pazu', 'Lusheeta Toel Ul Laputa']
            },
            {
                 'title': 'Grave of the Fireflies',
                 'actors': []
            }
        ]

        self.assertEqual(
            self.api_class()._extract_and_combine_films_and_actors(
                self.films_sample, self.actors_sample
            ),
            expected_output,
            "incorrect output format"
        )

    def get_mocked_resources(self, resource_name, fields=[]):
            return (
                self.films_sample if resource_name == "films"
                else self.actors_sample
            )

    @patch("films.views.cache")
    def test_calling_films_and_people_apis_when_films_are_not_cached(
        self, mocked_cache
    ):
        # when cache.get() is called return None
        mocked_cache.get.return_value = None

        mocked_external_api = MagicMock()
        get_resource_method = mocked_external_api.get_resource
        get_resource_method.side_effect = self.get_mocked_resources
        api_instance = self.api_class()
        api_instance.external_api = mocked_external_api

        dummy_request = Request(request=HttpRequest())
        api_instance.get(dummy_request)
        self.assertEqual(
            get_resource_method.call_count,
            2,
            "get_resource() should be called twice (/people and /films)"
        )

    @patch("films.views.cache")
    def test_not_calling_films_and_people_apis_when_films_are_cached(
        self, mocked_cache
    ):
        # when cache.get() is called return anything
        mocked_cache.get.return_value = self.output_sample

        mocked_external_api = MagicMock()
        get_resource_method = mocked_external_api.get_resource
        get_resource_method.return_value = {}
        api_instance = self.api_class()
        api_instance.external_api = mocked_external_api

        dummy_request = Request(request=HttpRequest())
        response = api_instance.get(dummy_request)
        self.assertEqual(
            mocked_external_api.get_resource.call_count,
            0,
            "get_resource() should not be called at all"
        )
        self.assertEqual(
            response.data,
            self.output_sample,
            "incorrect response"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "request is expected to be successful"
        )

    def test_return_500_when_films_and_people_couldn_not_be_fetched(
        self
    ):
        mocked_external_api = MagicMock()
        get_resource_method = mocked_external_api.get_resource
        get_resource_method.return_value = {}
        api_instance = self.api_class()
        api_instance.external_api = mocked_external_api

        dummy_request = Request(request=HttpRequest())
        response = api_instance.get(dummy_request)

        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "reponse should return 500"
        )