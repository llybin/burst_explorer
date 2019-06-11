FROM python:3.6.8-alpine

EXPOSE 5000 9001

ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

#RUN addgroup --system app && adduser --system --shell /bin/false --ingroup app app

RUN apk update && apk upgrade && apk add --no-cache bash

WORKDIR /app

#COPY --chown=app:app . .
COPY . .

RUN set -ex \
    && apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    mariadb-dev \
    linux-headers \
    && pip install pipenv==2018.11.26 uWSGI==2.0.18 supervisor==4.0.3 \
    && pipenv install --system --dev --deploy \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

#USER app

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["/usr/local/bin/supervisord", "-c", "supervisord.conf"]
