FROM docker.io/python:3.11-alpine

WORKDIR /app

RUN echo "DATABASE_URL: $DATABASE_URL"


COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check --no-build-isolation

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE:-config.settings}


COPY ./ /app


EXPOSE 8000

WORKDIR /app/server

# RUN python manage.py collectstatic 

RUN python manage.py collectstatic --noinput --clear

CMD ["gunicorn", "config.asgi:application", "-c", "conf.d/gunicorn.conf.py"]