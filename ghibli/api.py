import requests
from rest_framework import status

class GhibliAPI:

    base_url = "https://ghibliapi.herokuapp.com"
    fields_query_param = "?fields="

    def get_resource(self, resource_name, fields=[]):
        request_url = f"{self.base_url}/{resource_name}/"
        request_url = self._get_url_with_fields_query_param(
            request_url, fields
        )
        try:
            response = requests.get(request_url)
            return (
                response.json() if response.status_code == status.HTTP_200_OK else {}
            )
        except (
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError
        ):
            return {}

    def _get_url_with_fields_query_param(self, url, fields):
        if len(fields) > 0:
            fields_str = ",".join(fields)
            return url + f"{self.fields_query_param}{fields_str}"
        return url
