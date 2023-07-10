FROM python:3.10-alpine as prod-build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY poetry.lock pyproject.toml  /app/

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root


FROM python:3.10-alpine as prod-app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Copy installed required external packages from builded image
COPY --from=prod-build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=prod-build /usr/local/bin/ /usr/local/bin/

# Copy all project files
COPY . /app
WORKDIR /app

EXPOSE 5000

#RUN chmod +x docker-entrypoint.sh
CMD ["python3", "link_loader.py"]
