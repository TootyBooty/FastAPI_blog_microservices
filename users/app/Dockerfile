FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11

WORKDIR /users/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY --from=requirements-stage /tmp/requirements.txt /users/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /users/requirements.txt

RUN apt-get update && apt-get -y dist-upgrade

RUN apt install -y netcat-traditional

COPY ./entrypoint.sh /users/app/entrypoint.sh

RUN chmod +x entrypoint.sh

COPY ./ /users/app/


ENTRYPOINT ["sh", "/users/app/entrypoint.sh"]
