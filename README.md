# ZTP_final_project

## Requirements

* Python 3.6+
* Django and Django REST Framework
* DRF-YASG (Yet Another Swagger Generator)

```bash
pip install django djangorestframework drf-yasg
```

## Run app

Before running the app, you have to migrate data:

```bash
[ZTP_final_project/ztpfinal] $ python manage.py migrate
```

To run the app, use this command:

```bash
[ZTP_final_project/ztpfinal] $ python manage.py runserver
```

The site will be available on [localhost:8080](http://localhost:8080).

### Authentication

The app currently uses bearer token authentication provided by Django Rest Framework.

In order to create a user, send a JSON request to the `localhost:8000/register/` endpoint in the following form:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

The user is now created. In order to get the authentication token, send a request in the same form to `localhost:8000/login/`.
If the credentials are correct, you should get a response like this:

```json
{
  "token": "<YOUR_TOKEN>"
}
```

To use the protected endpoints (mostly POST), you will need to include the following header with the requests:
```
Authorization: Token <YOUR_TOKEN>
```

### Documentation

The Swagger API documentation is available at `/api-docs/`.