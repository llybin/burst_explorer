FROM python:3.6.8-alpine

EXPOSE 5000 9001

ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

RUN apk update && apk upgrade && apk add --no-cache bash pcre libxml2

WORKDIR /app

COPY . .

RUN set -ex \
    && apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    mariadb-dev \
    libc-dev \
    musl-dev \
    pcre-dev \
    zlib-dev \
    jpeg-dev \
    libffi-dev \
    libxml2-dev \
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

CMD ["/app/docker-entrypoint.sh"]
