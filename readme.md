# E-commerce Backend site with GraphQL and Django

## Description
The goal is to have a base project base with FastAPI. The project run on docker

## Settings
* Postgresql
* Redis

## Run projects

Please follow this part to start the project

### .env file for postgresql in .envs/.env.postgres
| Variable          | Description            | Default    |
|-------------------|------------------------|------------|
| POSTGRES_USER     | Postgres USERNAME      | test       |
| POSTGRES_PASSWORD | Postgres password      | passer1234 |
| POSTGRES_DB       | Postgres Database name | graphql    |
| POSTGRES_HOST     | Postgres host          | potsgres   |
| POSTGRES_PORT     | Postgres port          | 5432       |

### .env file for the app in .envs/.env.app
| Variable                    | Description                                                                    | Default             | Example        |
|-----------------------------|--------------------------------------------------------------------------------|---------------------|----------------|
| MAIL_USERNAME               | Email username                                                                 |                     | Test           |
| MAIL_FROM_NAME              | Test name                                                                      |                     | test name      |
| MAIL_SERVER                 | Email host                                                                     | mailhog             | smtp.gmail.com |
| MAIL_PORT                   | SMTP port                                                                      | 587                 |                |
| MAIL_TLS                    | Use TLS when sending email                                                     | False               |                |
| MAIL_FROM                   | Email user                                                                     | example@example.com |                |
| MAIL_PASSWORD               | Email password                                                                 | None                |                |
| LOG_FORMATTER               | Way to print your log. Colored (colored_formatter) or in JSON (json_formatter) | colored_formatter   |                |
| REDIS_DEFAULT_CACHE_DB      | Default Database for Django cache                                              | 5                   | 0              |
| JWT_SECRET_KEY              | JWT access secret key                                                          |                     |                |
| ACCESS_TOKEN_EXPIRE_MINUTES | Time duration  (in minute) of JWT key                                          |                     |                |
| JWT_REFRESH_SECRET_KEY      | JWT refresh secret key                                                         |                     |                |

