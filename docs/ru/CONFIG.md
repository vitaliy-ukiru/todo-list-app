# Настройки базы данных
При использовании docker-compose можно не устанавливать данные настройки,
т.к. они сами подставятся в файле docker-compose.

- `DB_PASSWORD` - Пароль для базы данных
- `DB_USERNAME` - Имя пользователя
- `DB_DATABASE` - Имя базы данных
- `DB_HOST` - Хост базы данных
- `DB_PORT` - Порт базы данных
- `REDIS_URL` - DSN до redis. Для хранения refresh tokens.

# Настройки механизма аутентификации
- `AUTH_PRIVATE_KEY_PATH` - Путь к файлу приватного ключа
- `AUTH_REFRESH_TOKEN_EXPIRES` - Время жизни refresh токена в [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). По умолчанию 30 дней.
- `AUTH_ACCESS_TOKEN_EXPIRES` - Время жизни access токена в [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). По умолчанию 5 минут.
- `AUTH_JWT_ALG` - Алгоритм для JWT семейства RSA. По умолчанию RS256

Все настройки кроме `AUTH_PRIVATE_KEY_PATH` рекомендуется оставить по умолчанию.

# Остальное
`API_HOST`, `API_PORT` - Хост и порт для запуска API

Если запускаете в докере, то чтобы сервер был доступен `API_HOST` должен быть 0.0.0.0 

