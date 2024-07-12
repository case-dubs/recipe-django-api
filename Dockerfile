# List of all docker python versions: https://hub.docker.com/_/python
FROM python:3.9-alpine3.13
LABEL maintainer="cDubsSubtidal"
# output from python logged directly to console
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt file from local machine to /tmp/requirements.txt into Docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy app directory that will contain our app to docker /app
COPY ./app /app
# Default directly that commands will be run from when we run commands on docker image
WORKDIR /app
# Expose port 8000 from docker to container to our local machine
EXPOSE 8000

# Creates a build argument and sets dev to false. By default, we're not running in development monde
ARG DEV=false
# Runs a command on python alpine image we're using.
# Specify a single run command broken into multiple lines for efficiency
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install postgresql client
    apk add --update --no-cache postgresql-client && \
    #sets virtual dependency package - we can use this to remove this later on once we no longer need them
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install requirements.txt to pip
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Now that requirements.txt is installed to pip, remove unused /tmp folder to save space and speed when deploying
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
        # fi ends if statement in shell file
        fi && \
    rm -rf /tmp && \
    # remove tmp-build-deps packages that were only temporarily needed. Keeps docker file lightweight and clean
    apk del .tmp-build-deps && \
    # adds a new user inside image.
    # Don't to use root user. If app gets compromised, then hacker gets full access to everything on docker container
    adduser \
        --disabled-password \
        --no-create-home \
        # Name of user
        django-user

# Defines directory where all commands are run
ENV PATH="/py/bin:$PATH"

# Specifies user we're switching to
USER django-user


