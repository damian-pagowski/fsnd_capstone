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
* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/


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