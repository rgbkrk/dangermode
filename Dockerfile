FROM jupyter/scipy-notebook

RUN pip install ipython fastapi jupyter-console uvicorn

WORKDIR /usr/src

COPY poetry.lock pyproject.toml README.md ./
COPY dangermode ./dangermode
RUN pip install -e .

WORKDIR /home/jovyan

EXPOSE 8000

CMD ["start.sh", "python", "-m", "dangermode", "--totally-in-docker"]
