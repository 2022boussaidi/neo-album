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