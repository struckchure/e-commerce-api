# e_commerce_api

[![AWS CI](https://github.com/struckchure/e_commerce_api/actions/workflows/aws-prod.yml/badge.svg)](https://github.com/struckchure/e_commerce_api/actions/workflows/aws-prod.yml)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5f625c005090486aa5915d9ab6e1d6d5)](https://app.codacy.com/gh/struckchure/e_commerce_api?utm_source=github.com&utm_medium=referral&utm_content=struckchure/e_commerce_api&utm_campaign=Badge_Grade_Settings)

e-commerce API built with Django Rest Framework.

## Features

- User registration and authentication
- Product listing and management
- Shopping cart
- Order management

## Upcoming features

- Payment integration
- Shipping methods
- Product reviews and ratings
- Store creation and management (although, out of scope for an e-commerce)

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
