FROM docker.io/library/alpine:latest

WORKDIR /app
RUN apk add --no-cache curl nginx supervisor uwsgi uwsgi-python3 python3 \
 && ln -s /usr/bin/python3 /usr/local/bin/python \
 && addgroup -g 1000 forumownik \
 && adduser -u 1000 -G forumownik -D -H forumownik

COPY requirements.txt /app/
RUN python -m venv venv \
 && source venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt

COPY --parents manage.py forumownik config /app/
RUN source venv/bin/activate \
 && ./manage.py collectstatic

COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/uwsgi.ini /etc/uwsgi.ini
COPY docker/nginx.conf /etc/nginx/http.d/default.conf
COPY docker/django.sh /django.sh

EXPOSE 80

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
