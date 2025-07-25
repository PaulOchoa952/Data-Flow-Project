# Running PostgreSQL with Docker Desktop on macOS

This guide explains how to quickly set up a PostgreSQL database using Docker Desktop on your Mac.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your Mac.

## Steps

### 1. Pull the PostgreSQL Docker Image

Open your terminal and run:

```
docker pull postgres:latest
```

### 2. Start a PostgreSQL Container

Run the following command to start a new PostgreSQL container:

```
docker run --name my-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=myuser -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres:latest
```

- `--name my-postgres`: Names your container (change as desired)
- `-e POSTGRES_PASSWORD=password`: Sets the database password (change for security)
- `-e POSTGRES_USER=myuser`: Sets the database user (change as needed)
- `-e POSTGRES_DB=mydatabase`: Sets the default database name
- `-p 5432:5432`: Maps port 5432 on your Mac to the container
- `-d`: Runs the container in detached mode
- `postgres:latest`: Uses the latest PostgreSQL image

### 3. Verify the Container is Running

Check running containers:

```
docker ps
```

You should see `my-postgres` listed.

### 4. Connect to PostgreSQL

You can connect using any PostgreSQL client (e.g., [Postico](https://eggerapps.at/postico/), [DBeaver](https://dbeaver.io/), or `psql`).

**Connection details:**
- Host: `localhost`
- Port: `5432`
- User: `myuser`
- Password: `password`
- Database: `mydatabase`

Or connect from the terminal using `psql` (if installed):

```
psql -h localhost -U myuser -d mydatabase
```

### 5. Stopping and Removing the Container

To stop the container:
```
docker stop my-postgres
```

To remove the container:
```
docker rm my-postgres
```

---

For more options and details, see the [official PostgreSQL Docker image documentation](https://hub.docker.com/_/postgres). 

The error message `zsh: command not found: psql` means that the `psql` command-line tool (the PostgreSQL client) is not installed on your Mac. While your PostgreSQL server is running in Docker, you need a client to connect to it from your terminal.

**Here’s how you can install `psql` on macOS:**

### Option 1: Install via Homebrew (Recommended)
If you have [Homebrew](https://brew.sh/) installed, run:
```sh
brew install libpq
brew link --force libpq
```
- `libpq` provides the `psql` client.
- The `brew link --force libpq` command makes `psql` available in your terminal.

### Option 2: Use Postgres.app (GUI + CLI)
- Download and install [Postgres.app](https://postgresapp.com/).
- After installation, add its binaries to your PATH (instructions are on their website).

### Option 3: Use Docker to Run `psql`
If you don’t want to install anything else, you can use the `psql` client inside another temporary Docker container:
```sh
docker run -it --rm --network=host postgres:latest psql -h localhost -U myuser -d mydatabase
```
- This will prompt you for the password (`password`).

---

**Summary:**  
- To use `psql` from your terminal, install it via Homebrew or Postgres.app.
- Alternatively, use Docker to run `psql` without installing anything extra.

## Importing Car Data with NiFi and PostgreSQL

### 1. PostgreSQL Table Structure

Run this SQL to create the table:

```sql
CREATE TABLE cars (
    brand varchar(255),
    price double precision,
    body varchar(255),
    mileage integer,
    engv double precision,
    engtype varchar(255),
    registration varchar(10),
    year integer,
    model varchar(255),
    drive varchar(255)
);
```

### 2. CSV Structure (No Header Row)
The CSV file should have columns in this order (no header row):

```
brand,price,body,mileage,engv,engtype,registration,year,model,drive
Ford,15500,crossover,68,2.5,Gas,yes,2010,Kuga,full
Mercedes-Benz,20500,sedan,173,1.8,Gas,yes,2011,E-Class,rear
...
```

### 3. NiFi CSVReader Controller Service Schema
Use the following Avro schema in the 'Schema Text' property:

```json
{
  "type": "record",
  "name": "cars",
  "fields": [
    { "name": "brand", "type": ["null", "string"] },
    { "name": "price", "type": ["null", "double"] },
    { "name": "body", "type": ["null", "string"] },
    { "name": "mileage", "type": ["null", "int"] },
    { "name": "engv", "type": ["null", "double"] },
    { "name": "engtype", "type": ["null", "string"] },
    { "name": "registration", "type": ["null", "string"] },
    { "name": "year", "type": ["null", "int"] },
    { "name": "model", "type": ["null", "string"] },
    { "name": "drive", "type": ["null", "string"] }
  ]
}
```
- Set 'Treat First Line as Header' to `false`.
- Set 'Value Separator' to `,`.
- Set 'Record Separator' to `\n`.

### 4. NiFi ReplaceText Processor (for NA → empty string)
- **Search Value:** `NA`
- **Replacement Value:** *(leave blank for empty string)*
- **Replacement Strategy:** `Literal Replace`
- **Evaluation Mode:** `Line-by-Line`

### 5. Flow Order
1. Input CSV → 2. ReplaceText (NA → empty) → 3. PutDatabaseRecord

---

This workflow ensures your car data is imported cleanly from CSV to PostgreSQL using NiFi, with correct handling of 'NA' values and matching data types.

ALTER TABLE cars
ALTER COLUMN registration TYPE varchar(10);
```

## Building a Secure API with FastAPI, PostgreSQL, and Keycloak

Here’s a high-level step-by-step plan to create a secure API using FastAPI, Docker, K8s, Python, Redis, Keycloak, and Swagger, integrating with your PostgreSQL database and NiFi dataflow:

### 1. Design Your API (Swagger/OpenAPI)
- Define your endpoints (e.g., `/cars`, `/cars/{id}`) and request/response models using OpenAPI/Swagger.
- FastAPI auto-generates Swagger UI at `/docs`.

### 2. Set Up FastAPI Project
- Create a new FastAPI project.
- Define Pydantic models matching your `cars` table.
- Implement endpoints for CRUD operations (GET, POST, PUT, DELETE) on cars.

### 3. Connect FastAPI to PostgreSQL
- Use an async ORM like SQLModel, SQLAlchemy, or Tortoise ORM.
- Configure the database connection string to your PostgreSQL instance (the one used by NiFi).

### 4. Add Redis Integration (Optional)
- Use Redis for caching, rate limiting, or session storage as needed.
- Install and configure a Redis client (e.g., `redis-py` or `aioredis`).

### 5. Secure the API with Keycloak
- Set up a Keycloak server (can be run in Docker).
- Create a realm, client, and user roles in Keycloak.
- Configure FastAPI to use OAuth2/OpenID Connect with Keycloak (use `fastapi-keycloak` or `python-jose` for JWT validation).
- Protect your endpoints with authentication and role-based authorization.

### 6. Dockerize the Application
- Write a `Dockerfile` for your FastAPI app.
- Add a `docker-compose.yml` if you want to run FastAPI, PostgreSQL, Redis, and Keycloak together locally.

### 7. Deploy to Kubernetes
- Write Kubernetes manifests (Deployment, Service, Ingress, ConfigMap/Secret for env vars).
- Deploy your containers (FastAPI, Redis, Keycloak, etc.) to your K8s cluster.

### 8. Test and Document with Swagger
- Access `/docs` on your FastAPI app to use Swagger UI.
- Test endpoints, including authentication with Keycloak tokens.

### 9. Integrate with NiFi (if needed)
- If you want NiFi to call your API, use NiFi’s InvokeHTTP processor.
- If you want your API to trigger NiFi, use NiFi’s ListenHTTP processor.

---

**Summary Table**

| Step | Task                                      | Tool/Tech         |
|------|-------------------------------------------|-------------------|
| 1    | Design API (OpenAPI/Swagger)              | FastAPI           |
| 2    | Implement FastAPI endpoints               | FastAPI, Python   |
| 3    | Connect to PostgreSQL                     | SQLAlchemy/ORM    |
| 4    | Integrate Redis (optional)                | Redis, redis-py   |
| 5    | Secure with Keycloak                      | Keycloak, OIDC    |
| 6    | Dockerize                                 | Docker            |
| 7    | Deploy to Kubernetes                      | K8s, manifests    |
| 8    | Test with Swagger UI                      | FastAPI           |
| 9    | Integrate with NiFi (optional)            | NiFi, HTTP        |

This plan will help you build a robust, secure, and scalable API integrated with your data pipeline.