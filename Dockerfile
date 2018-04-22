FROM python:3
EXPOSE 8000
ENV PYTHONUNBUFFERED 1

WORKDIR /web
COPY . /web

RUN pip install -r requirements.txt

RUN ./manage.py migrate --noinput
RUN ./manage.py collectstatic --noinput

ENV GUNICORN_CMD_ARGS '--bind=0.0.0.0:8000'
CMD gunicorn school_web.wsgi
