# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the application's source code into the container.
COPY . .

# Give the non-privileged user ownership of the application's source code.
RUN chown -R appuser:appuser /app && chmod -R 755 /app
RUN mkdir -p /nonexistent && \
    chown -R appuser:appuser /nonexistent && \
    chmod -R 755 /nonexistent

# Switch to the non-privileged user to run the application.
USER appuser

# Install the application's dependencies.
RUN pip install -e .

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD python ./src/main.py
