# FastAPI-Nextjs
[![codecov](https://codecov.io/gh/Nneji123/fastapi-webscraper/graph/badge.svg?token=UsIESnIqm6)](https://codecov.io/gh/Nneji123/fastapi-webscraper)

[![Python Tests](https://github.com/Nneji123/fastapi-webscraper/actions/workflows/test.yml/badge.svg)](https://github.com/Nneji123/fastapi-webscraper/actions/workflows/test.yml)

[![Python Tests](https://github.com/Nneji123/fastapi-webscraper/actions/workflows/test.yml/badge.svg)](https://github.com/Nneji123/fastapi-webscraper/actions/workflows/test.yml)


## Introduction
This project serves as a comprehensive demonstration of building a robust API using cutting-edge technologies, including FastAPI, SQLModel, PostgreSQL, Redis, Next.js, Docker, and Docker Compose. The goal is to showcase the implementation of essential API features, such as rate limiting and pagination, while maintaining a modular and scalable architecture.

## Technologies Used

- **FastAPI:** A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.

- **SQLModel:** An SQL database toolkit for FastAPI that provides a simple way to interact with databases using Python models.

- **PostgreSQL:** A powerful, open-source relational database system, chosen for its reliability and scalability.

- **Redis:** An in-memory data structure store used for caching and as a message broker.

- **Next.js:** A React framework for building server-side rendered and statically generated web applications.

- **Docker:** Containerization technology to ensure consistent deployment across different environments.

- **Docker Compose:** A tool for defining and running multi-container Docker applications.


## Features

1. **RESTful API Endpoints:**
   - Implemented CRUD operations for towns and people.
   - Defined RESTful API endpoints using FastAPI decorators.

2. **Database Integration:**
   - Integrated with a PostgreSQL database using SQLAlchemy.
   - Defined data models for towns and people.

3. **Data Pagination:**
   - Implemented pagination for large datasets for improved performance.

4. **Validation and Request Handling:**
   - Utilized FastAPI's automatic data validation.
   - Implemented request validation using Pydantic models.

5. **Rate Limiting:**
   - Implemented rate limiting for specific endpoints to control client requests.

6. **Dependency Injection:**
   - Leveraged FastAPI's dependency injection system for managing database sessions.


8.  **API Documentation:**
    - Generated API documentation using Swagger UI and ReDoc.
    - Documented request/response models, available endpoints, and usage examples.

9.  **Testing:**
    - Wrote unit tests and integration tests using Pytest.

10. **Dockerization:**
    - Dockerized the FastAPI application for consistent deployment environments.
    - Used Docker Compose for managing multi-container applications (frontend, postgres, redis).

11. **Database Migrations:**
    - Implemented database migrations using Alembic to manage schema changes.

12. **Cross-Origin Resource Sharing (CORS):**
    - Enabled CORS to control API access from different domains.

13. **Environmental Configuration:**
    - Used environment variables for configuration settings.

14. **Implemented frontend:**
    - Used Nextjs to develop a frontend to interact with the API. Utilized docker compose for communication between frontend and backend.

## Setup

### Cloning and Environment Setup
1. Clone the repository: `git clone https://github.com/Nneji123/fastapi-nextjs.git`
2. Navigate to the project directory: `fastapi-nexjs`
3. Create and activate a virtual environment:
   - Using `venv` on Linux: `python3 -m venv env && source env/bin/activate`
   - Using `venv` on Windows and Git Bash: `python3 -m venv env && source env/Scripts/activate`
4. Install dependencies: `cd backend && pip install -r api/requirements.txt`
5. Setup sqlite database: `python api/init_db.py`

### Setup Database Migrations with Alembic
Alembic is used in this project to handle schema changes in the database(add new columns, remove columns etc without deleting the database).

Assuming we're working in the backend directory:

1. Firstly run:  `alembic init -t sync migrations`
2. Within the generated "migrations" folder, import sqlmodel into script.py.mako since this project uses sqlmodel.
3. Import sqlmodel into the migrations/env.py file: `from sqlmodel import SQLModel` and also import your database tables in the same file:
```
from api.public.people.models import Person
from api.public.towns.models import Town
```
4. Set your metadata in the same file:
```
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata
```
5. To generate the first migration file, run: `alembic revision --autogenerate -m "init"`
6. Apply the migration: `alembic upgrade head`
7. To make changes to the database edit the models and then run steps 5 and 6 again.

### Running the API
1. Ensure you are in the project directory (`backend`).
2. Run the FastAPI application: `python api/asgi.py`
3. Access the API at `http://localhost:8000`

You should be able to see the swagger docs at `http://localhost:8000/docs`

### Running the Project Using Docker
1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project directory: `cd yourproject`
3. Build and start the containers: `docker-compose up --build`
4. Access the API at `http://localhost:8000` and the frontend built with nextjs and (https://v0.dev)[v0.dev] at `http://localhost:3000`


## Endpoints

<details>

### Get Single Person

- **Endpoint:** `GET /{person_id}`
- **Description:** Retrieves details of a single person by ID.
- **Request:**
  - Method: `GET`
  - Path: `/{person_id}` (Replace `{person_id}` with the actual ID)
- **Response:**
  - Status Code: `200 OK` if person is found, `404 Not Found` if person with the specified ID does not exist.
  - Body: Person details in the format specified by `PersonReadWithTown` model.

### Get All People

- **Endpoint:** `GET /`
- **Description:** Retrieves a paginated list of all people.
- **Request:**
  - Method: `GET`
  - Path: `/`
  - Query Parameters: `skip` (number of items to skip), `limit` (maximum number of items to return)
- **Response:**
  - Status Code: `200 OK`
  - Body: Paginated list of people in the format specified by `Page[PersonRead]` model.

### Create New Person

- **Endpoint:** `POST /`
- **Description:** Creates a new person.
- **Request:**
  - Method: `POST`
  - Path: `/`
  - Body: JSON object representing the new person (See `PersonCreate` model)
- **Response:**
  - Status Code: `200 OK` if successful, `500 Internal Server Error` if there's an exception during person creation.
  - Body: Created person details in the format specified by `Person` model.

### Update Existing Person

- **Endpoint:** `PUT /{person_id}`
- **Description:** Updates details of an existing person by ID.
- **Request:**
  - Method: `PUT`
  - Path: `/{person_id}` (Replace `{person_id}` with the actual ID)
  - Body: JSON object representing the updated person details (See `PersonUpdate` model)
- **Response:**
  - Status Code: `200 OK` if successful, `404 Not Found` if person with the specified ID does not exist.
  - Body: Updated person details in the format specified by `Person` model.

### Delete Existing Person

- **Endpoint:** `DELETE /{person_id}`
- **Description:** Deletes an existing person by ID.
- **Request:**
  - Method: `DELETE`
  - Path: `/{person_id}` (Replace `{person_id}` with the actual ID)
- **Response:**
  - Status Code: `200 OK` if successful, `404 Not Found` if person with the specified ID does not exist.
  - Body: Deleted person details in the format specified by `Person` model.

Please make sure to replace placeholders like `{person_id}` with actual values when making requests. Additionally, provide appropriate details in the request bodies according to your data models (`PersonCreate`, `PersonUpdate`, etc.).

### Create a New Town

- **Endpoint:** `POST /`
- **Description:** Creates a new town.
- **Request:**
  - Method: `POST`
  - Path: `/`
  - Body: JSON object representing the new town (See `TownCreate` model)
- **Response:**
  - Status Code: `200 OK` if successful, `500 Internal Server Error` if there's an exception during town creation.
  - Body:
    ```json
    {
      "status": "success",
      "msg": "Town created successfully",
      "data": { /* Town details */ }
    }
    ```

### Get Single Town

- **Endpoint:** `GET /{town_id}`
- **Description:** Retrieves details of a single town by ID.
- **Request:**
  - Method: `GET`
  - Path: `/{town_id}` (Replace `{town_id}` with the actual ID)
- **Response:**
  - Status Code: `200 OK` if town is found, `404 Not Found` if town with the specified ID does not exist.
  - Body: Town details in the format specified by `TownReadWithPeople` model.

### Get All Towns

- **Endpoint:** `GET /`
- **Description:** Retrieves a paginated list of all towns.
- **Request:**
  - Method: `GET`
  - Path: `/`
  - Query Parameters: `skip` (number of items to skip), `limit` (maximum number of items to return)
- **Response:**
  - Status Code: `200 OK`
  - Body: Paginated list of towns in the format specified by `Page[TownRead]` model.

### Update Existing Town

- **Endpoint:** `PUT /{town_id}`
- **Description:** Updates details of an existing town by ID.
- **Request:**
  - Method: `PUT`
  - Path: `/{town_id}` (Replace `{town_id}` with the actual ID)
  - Body: JSON object representing the updated town details (See `TownUpdate` model)
- **Response:**
  - Status Code: `200 OK` if successful, `404 Not Found` if town with the specified ID does not exist.
  - Body: Updated town details in the format specified by `TownRead` model.

### Delete Existing Town

- **Endpoint:** `DELETE /{town_id}`
- **Description:** Deletes an existing town by ID.
- **Request:**
  - Method: `DELETE`
  - Path: `/{town_id}` (Replace `{town_id}` with the actual ID)
- **Response:**
  - Status Code: `200 OK` if successful, `404 Not Found` if town with the specified ID does not exist.
  - Body:
    ```json
    {
      "status": "success",
      "msg": "Successfully deleted town with ID {town_id}"
    }
    ```
    or
    ```json
    {
      "status": "error",
      "msg": "Failed to delete town with ID {town_id}"
    }
    ```
Certainly! Here's a description for the rate-limited endpoint in your FastAPI project:

### Rate-Limited Endpoint

- **Endpoint:** `GET /rate_limit`
- **Description:** Returns a message indicating that this is a rate-limited endpoint. The endpoint is rate-limited to allow a maximum of 2 requests every 5 seconds.
- **Request:**
  - Method: `GET`
  - Path: `/rate_limit`
- **Response:**
  - Status Code: `200 OK` if the rate limit is not exceeded, `429 Too Many Requests` if the rate limit is exceeded.
  - Body:
    - If the rate limit is not exceeded:
      ```json
      {
        "Hello": "This is a rate-limited endpoint!"
      }
      ```
    - If the rate limit is exceeded:
      ```json
      {
        "detail": "Too many requests, try again later."
      }
      ```
- **Rate Limit:**
  - Maximum Requests: 2 requests per 5 seconds.

This endpoint is configured to limit the number of requests to 2 every 5 seconds, and it will respond with a success message if the rate limit is not exceeded. If the rate limit is exceeded, it will respond with a "Too Many Requests" error message.

</details>

## Deployment
For deployment I used Koyeb. Koyeb is a developer-friendly serverless platform to deploy apps globally. No-ops, servers, or infrastructure management. You can learn more about it here: `https://www.koyeb.com/tutorials/deploy-apps-using-docker-compose-on-koyeb`

Follow the steps below to deploy and run the docker-compose application on your Koyeb account.

### Requirements

You need a Koyeb account to successfully deploy and run this application. If you don't already have an account, you can sign-up for free [here](https://app.koyeb.com/auth/signup).

### Deploy using the Koyeb button

The fastest way to deploy the docker-compose application is to click the **Deploy to Koyeb** button below.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=fastapi-nextjs&privileged=true&type=git&repository=koyeb/example-docker-compose&branch=main&builder=dockerfile&dockerfile=Dockerfile.koyeb)

Clicking on this button brings you to the Koyeb App creation page with everything pre-set to launch this application.

### Fork and deploy to Koyeb

If you want to customize and enhance this application, you need to fork this repository.

If you used the **Deploy to Koyeb** button, you can simply link your service to your forked repository to be able to push changes.
Alternatively, you can manually create the application as described below.

On the [Koyeb Control Panel](//app.koyeb.com/apps), click the **Create App** button to go to the App creation page.

1. Select `GitHub` as the deployment method to use
2. In the repositories list, select the repository you just forked
3. Specify the branch to deploy, in this case `main`
4. Set the `Dockerfile location` to `Dockerfile.koyeb`
5. Set the `privileged` flag
6. Then, give your App a name, i.e `docker-compose-on-koyeb`, and click **Create App.**

You land on the deployment page where you can follow the build of your docker-compose application. Once the build is completed, your application is being deployed and you will be able to access it via `<YOUR_APP_NAME>-<YOUR_ORG_NAME>.koyeb.app`.

## Logging and Metrics

### Prometheus

[Prometheus](https://prometheus.io/) is used to collect and store metrics from your FastAPI application. It gathers data from various services and components, providing insights into the performance and behavior of your application.

#### Configuration

The Prometheus configuration is defined in the `prometheus_data/prometheus.yml` file. Make sure to customize this file based on your application's specific metrics and requirements.

#### Accessing Prometheus

Prometheus can be accessed at [http://localhost:9090](http://localhost:9090) in your local development environment.

### Grafana

[Grafana](https://grafana.com/) is utilized for visualizing and analyzing the metrics collected by Prometheus. It offers powerful tools for creating dashboards and monitoring the health of your application.

#### Configuration

No specific Grafana configuration is needed for basic functionality. However, you can customize Grafana settings and dashboards based on your monitoring needs.

To learn more about this you can read this article: https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn

#### Accessing Grafana

Grafana is accessible at [http://localhost:4000](http://localhost:4000) in your local development environment.

#### Default Credentials

- **Username:** admin
- **Password:** admin

### Metrics and Dashboards

Your FastAPI application is instrumented to expose relevant metrics, which are then visualized in Grafana dashboards. These metrics provide valuable insights into request/response times, error rates, and various aspects of your application's performance.

## Pagination
Pagination using FastAPI-Pagination is implemented in the get all towns and get all people routes.

## Testing
1. To run tests with in-memory SQLite database:
```
cd backend
pip install -r api/requirements.txt
python init_db.py
pytest tests
```
2. Check coverage with: `pytest --cov=yourmodule`

## To-Do
1. [x] Add pagination using FastAPI-Pagination
2. [x] Write test cases for the api.
3. [x] Add GitHub Actions template for running tests
4. [x] Write Makefile for easier project management
5. [x] Remove unnecessary files
6. [x] Abstract routes to a `public_routes.py` file
7. [x] Improve documentation for public routes API
8. [x] Add Alembic support for database migrations
9. [ ] Implement either Propelauth or FastAPI-Auth0 for authentication
10. [x] Implement rate limiting
11. [x] Allow CORS
12. [x] Write Docker and Docker Compose files for production deployment.
13. [ ] Replace current linter with "ruff".
14. [ ] Use bookmark to add code samples and change logo. generate logo with bing
15. [x] Create a new branch and remove async functionality for ease of use.
16. [x] Create a frontend with nextjs/reactjs showing how to use the api
17. [ ] Background tasks with celery
18. [ ] Logging with Prometheus and Grafana

## References
Certainly! Here are five FastAPI repositories with their names and links:

1. **Fast-Api-Grafana-Starter**
   - [Repository Link](https://github.com/KenMwaura1/Fast-Api-Grafana-Starter)

2. **prometheus-fastapi-instrumentator**
   - [Repository Link](https://github.com/trallnag/prometheus-fastapi-instrumentator)

3. **fastapi-keycloak**
   - [Repository Link](https://github.com/code-specialist/fastapi-keycloak)
Certainly! Here are five more FastAPI repositories with their names and links:

4. **propelauth-fastapi**
   - [Repository Link](https://github.com/PropelAuth/propelauth-fastapi)

5. **Shortify**
   - [Repository Link](https://github.com/IHosseini083/Shortify)

6. **fastapi-beanie-jwt**
   - [Repository Link](https://github.com/flyinactor91/fastapi-beanie-jwt)

7. **fastapi-best-practices**
   - [Repository Link](https://github.com/zhanymkanov/fastapi-best-practices)

8. **fastapi-sqlmodel-alembic**
    - [Repository Link](https://github.com/testdrivenio/fastapi-sqlmodel-alembic)

## License
This project is licensed under the MIT LICENSE - see the [LICENSE](./LICENSE) file for details.

