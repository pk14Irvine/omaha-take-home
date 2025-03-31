# Omaha Take Home: EcoVision: Climate Visualizer Backend

The backend for the EcoVision app utilizes FastApi. For a full api spec please see: http://127.0.0.1:8000/docs

## Project Dependencies

- fastapi
- python 3.13.1
- venv
- postgres 17

## Getting Started

### Server Life Cycle

```mermaid
    sequenceDiagram
        actor dev as Developer
        participant fp as FastApi
        participant lf as Lifecycle Hook
        participant rl as Routing Layer
        participant dl as Data Access Layer

        dev->>fp: server startup
        fp->lf: trigger startup lifecycle hook
        lf->>lf: log server boot
        alt environment == dev
            lf->>dl: init db
            dl->>dl: create tables & seed data
            dl-->>lf: setup complete
        end
        lf->>fp: yield async startup
        fp->>rl: app startup ready
        loop
            rl->>rl: process requests
        end
        dev->>fp: kill server
        fp->>lf: trigger kill server event <br>and retrigger from yield point
         alt environment == dev
            lf->>dl: drop tables
            dl->>dl: drop tables
            dl-->>lf: drop complete
        end
        lf->>fp: event complete
        fp->>dev: server terminated
```

### 1. Activate venv

Start virtual environment to encapsulate dependencies:

`source .venv/bin/activate`

### 2. Install Requirements

Install package dependencies via pip declared in requirements.txt:

`pip install -r requirements.txt`

### 3. Server Startup

Use the .env file to load environment files. If the `ENVIRONMENT` is dev, the startup script will load the seed data.

#### Production Startup

`fastapi run app.py`

#### Dev Startup

`fastapi dev app.py`

#### Dev Startup With Hot Reload

`fastapi dev app.py --reload`

## Unit Testing

The test suite leverages PyTest. To run the suite use:

`pytest`

## Architecture

### Entity Relationship Diagram

```mermaid
erDiagram
    LOCATIONS {
        int ID
        string NAME
        string COUNTRY
        double LATITUDE
        double LONGITUDE
        string REGION
    }

    METRICS {
        int ID
        string NAME
        string DISPLAY_NAME
        string UNIT
        string DESCRIPTION
    }

    CLIMATE_DATA {
        int ID
        int LOCATION_ID
        int METRIC_ID
        date DATE
        double VALUE
        string QUALITY
    }

    LOCATIONS ||--o| CLIMATE_DATA : refers
    METRICS ||--o| CLIMATE_DATA : refers

```

### Sequence Diagram

```mermaid
    sequenceDiagram
        actor us as User
        participant fe as Frontend
        participant be as Backend
        participant pg as Postgres

        us->>fe: refresh dashboard
        fe->>be: fetch data
        be->>pg: query for data
        pg-->>be: query response
        be-->>fe: return response
        fe-->>us: hydrate ui
```

## Decisions

1. Use FastApi has the underlying framework.

- Reasons:
  - Good dev ex and easy for other developers to onboard
  - Stronger familiarity
  - Fast startup speed + easy access to server lifecycle
  - Route based project structuring becomes simpler

2. Use Postgres for DB

- Reasons:
  - Relational query model is better suited for the OLAP style query pattern
  - Data has strong relational dependencies
  - Postgres has great community support and documentation

3. Create a Data Access Layer (DAL) to interface out queries

- Reasons:
  - Provides a strong interface in case our data source changes at any time in the future.
  - Simplify access patterns from the routing logic
  - Draw clearer lines around application boundary

4. Use SQL Model as the SQL Driver

- Reasons:
  - SQL Model supports almost all SQL databases and even some NoSQL DBs. It can be used as a good interface for queries.
  - Good community support and easy integration points with FastApi. Same creator!
  - Offers ORM style query patterns and raw query execution. Class based definitions were used to define the schema in place while more complicated queries used raw SQL.

5. Unit Testing via Pytest

- Reasons:
  - PyTest is a simple and commonly used framework
  - Easy to run with FastApi

## Improvements

1. Schema Improvements:

- Pull out quality threshold into it's own table and introduce and index value.
- Introduce indexes around name and common join points

2. Write more Unit Tests:

- The PyTest integration is started and the base route is being tested but more unit tests can be added

3. Leverage async more in the APIs

- Concurrent requests can be handled better since this application is proxying a lot of requests to the DB.
