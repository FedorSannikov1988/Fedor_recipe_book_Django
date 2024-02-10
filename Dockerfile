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
RUN pip install -r requirements.txt

# Copy the project files into the container at /app
COPY ./fedor_recipe_book/. /app/.

ENV IP_ADDRESS=${IP_ADDRESS}
ENV DJANGO_PORT=${DJANGO_PORT}
ENV SECRET_KEY=${SECRET_KEY}
ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_PORT=${EMAIL_PORT}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}

CMD ["python3", "manage.py", "runserver"]
