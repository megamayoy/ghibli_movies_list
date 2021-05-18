![](logo.png)

Studio Ghibli Inc. is a Japanese animation film studio headquartered in Koganei, Tokyo. The studio is best known for its animated feature films.

They offer a ​[REST API](https://ghibliapi.herokuapp.com/) where information
about movies and people (characters) can be queried.

An API is created (/movies) using Django Rest framework that consumes their people and films API endpoints to display all movies and the characters of each movie.

Preview the API documentation for more details(Studio_Ghibli_Movies_List_API.yaml)

## Installation Guide
Python version: 3.6
### Create a virtualenv, activate it, install dependencies and run the server
make sure you navigate to the repository before running the commands below
```bash
$ virtualenv venv -p=python3.6
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./manage.py runserver
then navigate to localhost:8000/movies in the browser to see the results
```

### Architecture explained
It was a part of the requirements that data retrieved from the Ghibli API endpoints shouldn't be more than 1 minute older so,
due to intesive API calls, no database is used.A cache layer is used instead to keep the data retrieved from Ghibli APIs for one minute before calling them again.
