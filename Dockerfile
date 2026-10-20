FROM docker.io/library/python:3.15-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY --parents entrypoint.sh manage.py forumownik config /app/

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
