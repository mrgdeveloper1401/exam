FROM async_django:1.2.0

WORKDIR /app

COPY . .

RUN adduser -D -H mohammad && \
    chown -R mohammad:mohammad /app && \
    pip install psycopg2-binary

USER mohammad