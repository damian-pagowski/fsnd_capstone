# Casting Agency


### Description
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Technology Stack

* App: Python, Flask
* Database: SQLlite, SqlAlchemy
* IAM: Auth0
* Hosting: application is Heroku deployable (check: Procfile)


## Installation

Set up environment variables

```bash
./setup.sh
```
Install dependencies

```bash
pip install -r requirements.txt 
```

## Usage

Start API server:

```python
python app.py
```
## Data Models:

* Movies with attributes title and release date
* Actors with attributes name, age and gender

## API Endpoints:
#### GET /actors
* Parameters: none
* Example response 
```
{
  "actors": [
    {
      "age": 100,
      "gender": "M",
      "id": 1,
      "movie_id": 1,
      "name": "Stallone"
    }
  ],
  "success": true
}
```
#### GET /movies
* Parameters: none
* Example response 
```
{
  "movies": [
    {
      "actors": [
        {
          "age": 100,
          "gender": "M",
          "id": 1,
          "movie_id": 1,
          "name": "Stallone"
        }
      ],
      "id": 1,
      "relese_date": "1980",
      "title": "Rambo"
    }
  ],
  "success": true
}
```
#### POST /movies 
* request body
```
{"title": "Rambo", "relese_date" : 1980}
```
* response
```
{
  "movie": {
    "actors": [],
    "id": 1,
    "relese_date": "1980",
    "title": "Rambo"
  },
  "success": true
}
```
#### POST /actors 
* Request body:
```
{
    "name": "Stallone",
    "age": "100",
    "gender": "M",
    "movie_id": 1
}
```
* Example response
```
{
  "actor": {
    "age": 100,
    "gender": "M",
    "id": 1,
    "movie_id": 1,
    "name": "Stallone"
  },
  "success": true
}
```

#### DELETE /actors/<id>

* Parameters: actor_id
* Example response 
```
{
  "status": "deleted",
  "success": true
}
```

#### DELETE /movies/<id>

* Parameters: movie_id
* Example response 
```
{
  "status": "deleted",
  "success": true
}
```
#### PATCH /actors/<id>

* Parameters: actor_id
* Request body example:
```
{
"name": "Stallone", 
"age": "150"
}
```
* Example response 
```
{
  "actor": {
    "age": 150,
    "gender": "M",
    "id": 1,
    "movie_id": 1,
    "name": "Stallone"
  },
  "success": true
}
```
#### PATCH /movies/<id>

* Parameters: movie_id
* Request body example:
```
{"title": "Rambo", "relese_date" : 1983}
```
* Example response 
```
{
  "movie": {
    "actors": [
      {
        "age": 150,
        "gender": "M",
        "id": 1,
        "movie_id": 1,
        "name": "Stallone"
      }
    ],
    "id": 1,
    "relese_date": "1983",
    "title": "Rambo"
  },
  "success": true
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## IAM

### Roles
* Casting Assistant
Can view actors and movies

* Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies

* Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database


## Testing



## License
[MIT](https://choosealicense.com/licenses/mit/)