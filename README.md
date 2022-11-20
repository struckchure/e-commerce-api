# e_commerce_api

[![AWS CI](https://github.com/struckchure/e_commerce_api/actions/workflows/aws-prod.yml/badge.svg)](https://github.com/struckchure/e_commerce_api/actions/workflows/aws-prod.yml)

e-commerce API built with Django Rest Framework. It provides the following features:

- User registration and authentication
- Product listing and management
- Shopping cart
- Order management

## Upcoming features

- Payment integration
- Shipping integration
- Product reviews and ratings
- Store creation and management

## Installation

You need to have docker and docker-compose installed on your machine.

Clone the repository and run the following command:

For development:

```bash
$ docker-compose -f docker-compose.dev.yml up --force-recreate --build
```

For production:

```bash
$ docker-compose up --force-recreate --build
```

This will start the Django server on port 8000.
