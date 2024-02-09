# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y pkg-config
RUN apt-get install -y python3 python3-pip python3-venv libmariadb-dev-compat gcc && \
    rm -rf /var/lib/apt/lists/*
RUN python -m venv .venv
# RUN .venv/bin/pip install --upgrade pip
# RUN .venv/bin/pip install -r requirements.txt
RUN pip install -r requirements.txt

# Copy the project files into the container at /app
COPY fedor_recipe_book/ /app/fedor_recipe_book

# Expose the port on which the Django app will run
ARG DJANGO_PORT
EXPOSE $DJANGO_PORT

# Define the command to run the Django application
CMD ["manage.py", "runserver", "0.0.0.0:$DJANGO_PORT"]