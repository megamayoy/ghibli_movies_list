from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from ghibli.api import GhibliAPI

class FilmsList(APIView):
    def __init__(self, **kwargs):
        self.external_api = GhibliAPI()

    def get(self, request):
        cashed_films = cache.get('films')
        if cashed_films:
            return Response(cashed_films, status=status.HTTP_200_OK)
        characters = self.external_api.get_resource(
            "people", fields=["id","name","films"]
        )
        films = self.external_api.get_resource(
            "films", fields=["id", "title"]
        )
        if characters == {} or films == {}:
            return Response(
                {
                    "error": "An Error occured while calling external API"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        final_result = self._extract_and_combine_films_and_characters(
            films, characters
        )
        cache.set('films', final_result,timeout=60)
        return Response(final_result, status=status.HTTP_200_OK)

    def _extract_and_combine_films_and_characters(self, films, characters):
        films_dict = {}
        for film in films:
            film_id = film["id"]
            film.pop("id")
            films_dict[film_id] = film
            films_dict[film_id]["characters"] = []

        for character in characters:
            for film in character["films"]:
                film_id = film.split('/')[-1]
                films_dict[film_id]["characters"].append(character["name"])
        return list(films_dict.values())
