# SQLModel FastAPI Project

## Overview
This project utilizes FastAPI along with SQLModel, Asyncpg, SQLAlchemy, FastAPI-Limiter, FastAPI-Pagination, Docker, Docker Compose, Makefile, and Pytest for automated testing. It's deployed on Render using Docker.

## Features
- Feature 1: Description of feature 1
- Feature 2: Description of feature 2
- ...

## Setup

### Cloning and Environment Setup
1. Clone the repository: `git clone https://github.com/yourusername/yourproject.git`
2. Navigate to the project directory: `cd yourproject`
3. Create and activate a virtual environment:
   - Using `venv`: `python3 -m venv env && source env/bin/activate`
   - Using `conda`: `conda create --name envname python=3.8 && conda activate envname`
4. Install dependencies: `pip install -r requirements.txt`

### Running the Project Using Python API/ASGI
1. Ensure you are in the project directory.
2. Run the FastAPI application: `python api/asgi.py`
3. Access the API at `http://localhost:8000`

### Running the Project Using Docker
1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project directory: `cd yourproject`
3. Build and start the containers: `docker-compose up --build`
4. Access the API at `http://localhost:8000`

## Usage

### Endpoints
- **Endpoint 1**: Description of endpoint 1
- **Endpoint 2**: Description of endpoint 2
- ...

### Pagination
Pagination using FastAPI-Pagination is yet to be implemented.

### Testing
1. To run tests with in-memory SQLite database: `pytest`
2. Check coverage with: `pytest --cov=yourmodule`

## To-Do
1. [ ] Add pagination using FastAPI-Pagination
2. [ ] Write test cases for all routes and functions in the public model using an in-memory database
3. [x] Add GitHub Actions template for running tests
4. [x] Write Makefile for easier project management
5. [x] Remove unnecessary files
6. [x] Abstract routes to a `public_routes.py` file
7. [ ] Improve documentation for public routes API
8. [x] Add Alembic support for database migrations
9. [ ] Implement either Propelauth or FastAPI-Auth0 for authentication
10. [ ] Implement rate limiting
11. [x] Allow CORS
12. [x] Write Docker and Docker Compose files for production deployment.
13. [ ] Replace current linter with "ruff".
14. [ ] Use bookmark to add code samples and change logo. generate logo with bing
15. [ ] Create a new branch and remove async functionality for ease of use.

## Contribution
Feel free to contribute by opening issues or creating pull requests.

## License
This project is licensed under the MIT LICENSE - see the [LICENSE](./LICENSE) file for details.

