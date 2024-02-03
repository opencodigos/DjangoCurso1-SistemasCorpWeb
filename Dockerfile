FROM python:3.9-alpine3.13 
LABEL maintainer="Sistema Corporativo"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./SistemaCorp /SistemaCorp
COPY ./scripts /scripts

WORKDIR /SistemaCorp
EXPOSE 8000

RUN apk add --update --no-cache postgresql-client git openssh-client

RUN mkdir ~/.ssh/ && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

RUN apk add --no-cache su-exec

RUN --mount=type=ssh python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    mkdir -p /logs && \
    chown -R app:app /vol && \
    chown -R app:app /vol/web && \
    chown -R app:app /logs && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

# USER app

CMD ["run.sh"]