# todo_test

1. create any database
2. call `python manage.py migrate` - to migrate tables
3. call `python manage.py loaddata statuses.json` - to init statuses
4. create .env file (if you use it) and set following keys:
    - REDIS_HOST=0.0.0.0
    - REDIS_PORT=6379
    - ACCESS_TOKEN_LIFETIME_MINUTES=ANY
    - REFRESH_TOKEN_LIFETIME_DAYS=ANY
    - EMAIL_HOST=ANY
    - EMAIL_HOST_USER=ANY
    - EMAIL_HOST_PASSWORD=ANY
    - EMAIL_PORT=ANY
    - DB_NAME=ANY
    - DB_USER=ANY
    - DB_PASSWORD=ANY
    - DB_HOST=0.0.0.0
    - DB_PORT=5432
    - SECRET_KEY