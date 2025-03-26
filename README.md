# Neonumy Photo Album (Flask Version)

A simple photo album application built with Flask and PostgreSQL.

## Features

- Upload images
- View all images as thumbnails
- View image details in full size
- Delete images
- GraphQL API for all CRUD operations

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository
2. Run `docker-compose up --build`
3. Initialize the database:
   ```bash
   docker-compose run web flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
4. docker-compose exec db1 psql -U neonumy -d neonumy -c "SELECT * FROM photo;"

## Access the Web Application
http://localhost:5000

## Check GraphQL API 
http://localhost:5000/graphql

## run tests
1. pytest -v