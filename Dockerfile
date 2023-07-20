#FROM python:3.10-alpine as prod-build
#
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1
#
#WORKDIR /app
#
#RUN pip install --upgrade pip && \
#    pip install poetry
#
#COPY poetry.lock pyproject.toml  /app/
#
#RUN poetry config virtualenvs.create false
#RUN poetry install --no-interaction --no-ansi --no-root
#

#FROM python:3.10-alpine as prod-app
#
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1
#
## Copy installed required external packages from builded image
#COPY --from=prod-build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
#COPY --from=prod-build /usr/local/bin/ /usr/local/bin/
#
## Copy all project files
#COPY .. /app
#WORKDIR /app
#
#EXPOSE 5000
#
##RUN chmod +x docker-entrypoint.sh
#CMD ["python3", "linker_app", "--message-queue", "redis://redis:6379/", "--host", "0.0.0.0", "--port", "5000", "--cors-allowd-origins" , "*"]
#

FROM python:3.10-alpine as prod-build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY poetry.lock pyproject.toml  /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root


## Copy installed required external packages from builded image
#COPY --from=prod-build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
#COPY --from=prod-build /usr/local/bin/ /usr/local/bin/

# Copy all project files
COPY .. /app
RUN poetry install --no-interaction --no-ansi

EXPOSE 5000

#RUN chmod +x docker-entrypoint.sh
CMD ["poetry", "run" ,"app", "--message-queue", "redis://redis:6379/", "--host", "0.0.0.0"]
#CMD ["python3", "linker_app", "--message-queue", "redis://redis:6379/", "--host", "0.0.0.0", "--port", "5000", "--cors-allowd-origins" , "*"]
