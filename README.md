# Coderr Backend

## Description

Coderr Backend is a REST API built with Django and Django REST Framework.

The project provides user authentication, profile management, offer management, order processing and review functionality for the Coderr marketplace.

Authentication is implemented using Django REST Framework Token Authentication.

---

## Features

* User registration
* User login
* Token authentication
* Custom user model
* Customer and business profiles
* Offer management
* Order management
* Review management
* Base information endpoint
* Filtering with django-filter

---

## Tech Stack

* Python 3.13+
* Django 6
* Django REST Framework
* DRF Token Authentication
* SQLite3
* django-filter
* django-cors-headers
* python-dotenv

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd coderr-backend
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root based on the provided `.env.template`.

**Windows**

```bash
Copy-Item .env.template .env
```

**Linux / macOS**

```bash
cp .env.template .env
```

The project automatically loads environment variables from the `.env` file using `python-dotenv`.

---

## Database Setup

Apply the migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

---

## Run the Development Server

```bash
python manage.py runserver
```

The server will be available at:

```text
http://127.0.0.1:8000/
```

---

## Authentication

The API uses **Token Authentication**.

After a successful registration or login, the response contains an authentication token.

Include the token in every authenticated request:

```text
Authorization: Token <your_token>
```

---

## API Endpoints

### Authentication

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/api/registration/` |
| POST   | `/api/login/`        |

### Profiles

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | `/api/profile/{id}/`      |
| PATCH  | `/api/profile/{id}/`      |
| GET    | `/api/profiles/business/` |
| GET    | `/api/profiles/customer/` |

### Offers

| Method | Endpoint                  |
| ------ | ------------------------- |
| GET    | `/api/offers/`            |
| POST   | `/api/offers/`            |
| GET    | `/api/offers/{id}/`       |
| PATCH  | `/api/offers/{id}/`       |
| DELETE | `/api/offers/{id}/`       |
| GET    | `/api/offerdetails/{id}/` |

### Orders

| Method | Endpoint                                         |
| ------ | ------------------------------------------------ |
| GET    | `/api/orders/`                                   |
| POST   | `/api/orders/`                                   |
| PATCH  | `/api/orders/{id}/`                              |
| DELETE | `/api/orders/{id}/`                              |
| GET    | `/api/order-count/{business_user_id}/`           |
| GET    | `/api/completed-order-count/{business_user_id}/` |

### Reviews

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/reviews/`      |
| POST   | `/api/reviews/`      |
| PATCH  | `/api/reviews/{id}/` |
| DELETE | `/api/reviews/{id}/` |

### Base Information

| Method | Endpoint          |
| ------ | ----------------- |
| GET    | `/api/base-info/` |

---

## Project Structure

```text
Coderr/
├── auth_app/
├── base_info_app/
├── core/
├── offers_app/
├── orders_app/
├── profile_app/
├── reviews_app/
├── .env.template
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

Each application contains its own

* models.py
* admin.py
* api/

  * serializers.py
  * views.py
  * permissions.py
  * urls.py
* tests/

following Django REST Framework best practices.

---

## Permissions

Customer users can:

* create orders
* manage their own profile
* create reviews

Business users can:

* create and manage offers
* manage incoming orders
* manage their own profile

Permissions are enforced using custom Django REST Framework permission classes.

---

## Testing

The project was developed using a **Test Driven Development (TDD)** workflow.

Tests are organized into **Happy Path** and **Unhappy Path** scenarios to verify both expected behavior and proper error handling.

Run all tests:

```bash
python manage.py test
```

Run the tests for a specific app (example):

```bash
python manage.py test offers_app
```

Run a specific test module:

```bash
python manage.py test orders_app.tests.test_order_list_create_happy
```

---

## Development Notes

The project follows:

* Test Driven Development (TDD)
* Django REST Framework
* ModelSerializer for CRUD operations
* Token Authentication
* Environment variables using `python-dotenv`
* Separation of concerns
* RESTful API design
* Role-based permissions
* Filtering with `django-filter`

Requests were additionally verified in Postman during development.

The main endpoint validation is covered by automated Django and Django REST Framework tests.

---

## Notes

* SQLite is used as the default database.
* The `.env` file is excluded from version control.
* Create your own `.env` file using the provided `.env.template`.
* CORS is configured for local frontend development.

---

## Author

Nadine Bauer
