FROM async_django:1.2.0

WORKDIR /app

COPY . .

RUN chmod +x scripts/* && \
    adduser -D -H mohammad && \
    chown -R mohammad:mohammad /app

USER mohammad