FROM python:3.6.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get -y install --no-install-recommends libssl-dev python3-dev default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install pipenv==2018.11.26
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --dev --deploy

COPY . .

CMD [ "python manage.py runserver 0.0.0.0:8000" ]
