# Movie Collection API

This is a Django-based REST API for managing a collection of movies. The API allows users to perform CRUD operations on movie entries, integrate with an external movie listing API, and manage user authentication.



## Installation

1. Clone the repository:

```bash
git clone git@github.com:hencydsouza/movie-api.git
```
    
2. Navigate to the project directory:

```bash
cd movie-api
cd movie_collection_api
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```
## Usage

```bash
python manage.py runserver
```


## API Reference

#### Register a new user

```http
  POST /api/register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Login

```http
  POST /api/token/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Refreshtoken

```http
  POST /api/token/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `refresh` | `string` | **Required**. your refresh token |