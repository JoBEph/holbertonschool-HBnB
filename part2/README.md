# **Part 2 HbnB project**

## Description :
This part setup for a structured Python project designed to develop an "HBnB" web application, similar to Airbnb. The primary goal is to establish a clear and modular architecture, facilitating development, maintenance, and scalability.

## Concepts and Technologies :
- [x] **Flask** and **Flask-Restx**: Used to create the web application and REST API. <br/>
- [x] Facade design Pattern: Simplifies interactions between different application layers <br/>
- [x] In-Memory Data Repository :  A temporary solution for storing data, to be replaced by a database later. <br/>

## Objectives :
- Establish a solid and scalable architecture. <br/>
- Facilitate application development and maintenance. <br/>
- Prepare for database integration. <br/>

## Directory structure :

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

### `app/`
Contains and repertory the core application code. <br/>

---

### `app/api/v1`
Contain all manages REST API Endpoint. <br/>

---

#### `app/api/v1/users.py`
- File is created to define the user API Endpoint <br/>

The **POST** Endpoint is implemented to create new users.<br/>
The **GET**  Endpoint is implemented to retrieve the list of users. <br/>
The **GET** `<user_id>` Endpoint is implemented to retrieve a user by their ID. <br/>
The **PUT** `<user_id>` Endpoint is implemented to update user informations.

- Exemple:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```
#### `app/api/v1/place.py`
- File create to define the Place API Endpoint.<br/>

The **POST** Enpoint is implemented to create new place.<br/>
The **GET**  Endpoint is implemented to retrieve all places. <br/>
The **GET** `place_id` Endpoint is implemented to retrieve details of a specific place, including the owner and amenities. <br/>
The **PUT** Update Places informations. <br/>
- Exemple:
```http
POST /api/v1/places/
Content-Type: application/json

{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
#### `app/api/v1/amenity.py`
- The file create the amenity API Endpoint.
The **POST** Enpoint is implemented to create new Amenitys for places.<br/>
The **GET**  Endpoint is implemented to retrieve lists of amenitys. <br/>
The **GET** `amenity_id` Amenitys details. <br/>
The **PUT** Update Amenitys informations. <br/>
- Exemple :
```http
POST /api/v1/amenities/
Content-Type: application/json

{
  "name": "Wi-Fi"
}
```
#### `app/api/v1/reviews.py`
- The file create the Reviews API Endpoint.
The **POST** Enpoint is implemented to create new Reviews for places by users.<br/>
The **GET**  Endpoint is implemented to retrieve lists of Reviews. <br/>
The **GET** `<review_id>` Reviews details. <br/>
The **GET** `<place_id>/reviews` List Review from place. <br/> 
The **PUT** Update Reviews Details. <br/>
The **Delete** Delete a Reviews from place. <br/>

- Exemple :
```http
PUT /api/v1/reviews/<review_id>
Content-Type: application/json

{
  "text": "Amazing stay!",
  "rating": 4
}
```
---

### `app/models`
Define Data Models (Users, Place, Amenity, Review). <br/>

### `app/services`
Implements the Facade design pattern to manage interactions between different application layers. <br/>

### `app/persistence`
Manages data persistence (initially in-memory, later via a database). <br/>

### `requierments.txt`
Lists of packages needed to install for this project.<br/>
Contains: **Flask** and **Flask-Restx**.</br>

```
pip install -r requierments.txt
```
### `config.py`
Manages configuration settings <br/>

### `run.py`
The entry point for running the application <br/>
