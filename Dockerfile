FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

COPY app/ .

RUN pip install poetry
RUN poetry install --no-interaction --no-ansi --no-root

# CMD python main.py
CMD echo Buildou && sleep infinity
