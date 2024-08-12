# Database Settings
When using docker-compose, you don't have to set these settings,
because they will be substituted themselves in the docker-compose.

- `DB_PASSWORD` - Password for the database
- `DB_USERNAME` - Username
- `DB_DATABASE` - Database name
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `REDIS_URL` - DSN to redis. For storing refresh tokens.
- 
# Authentication Mechanism Settings
- `AUTH_PRIVATE_KEY_PATH` - Path to the private key file
- `AUTH_REFRESH_TOKEN_EXPIRES` - Lifetime of a refresh token in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). Default is 30 days.
- `AUTH_ACCESS_TOKEN_EXPIRES` - Lifetime of an access token in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). Default is 5 minutes.
- `AUTH_JWT_ALG` - Algorithm for JWTs of the RSA family. Default RS256

It is recommended to leave all settings except `AUTH_PRIVATE_KEY_PATH` at default.

# Other
`API_HOST`, `API_PORT` - Host and port for running the API