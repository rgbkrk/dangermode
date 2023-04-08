FROM python:3.9

RUN pip install poetry --no-cache-dir

WORKDIR /usr/src

COPY poetry.lock pyproject.toml README.md ./
COPY dangermode ./dangermode

RUN poetry install --no-dev

EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "dangermode"]