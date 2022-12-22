FROM python:3.9-alpine3.17
LABEL maintainer="gaby.es.sd@gmail.com"

ENV PYTHONUNBUFFERED 1

ARG APP_USER=app
ARG APP_GROUP=app
ARG APP_USER_UID=1003
ARG APP_GROUP_GID=1003

ENV APP_USER=${APP_USER}
ENV APP_GROUP=${APP_GROUP}
ENV APP_USER_UID=${APP_USER_UID}
ENV APP_GROUP_GID=${APP_GROUP_GID}

COPY ./requirements.txt /requirements.txt
COPY ./app /app
# COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --upgrade --no-cache postgresql-client libstdc++ && \
    apk add --upgrade --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    addgroup -g $APP_GROUP_GID -S $APP_GROUP && \
    adduser -u $APP_USER_UID -G $APP_GROUP --disabled-password --no-create-home $APP_USER && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R $APP_USER:$APP_USER /vol && \
    chmod -R 755 /vol
    # chmod -R +x /scripts

COPY ./base-media /base-media

ENV PATH="/py/bin:$PATH"
# ENV PATH="/scripts:/py/bin:$PATH"

USER $APP_USER

# CMD [ "run.sh" ]