# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . .

RUN apt-get update && apt-get install -y pkg-config
RUN apt-get install -y python3 python3-pip python3-venv libmariadb-dev-compat gcc --fix-missing &&  \
    rm -rf /var/lib/apt/lists/*
RUN python -m venv .venv
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt
RUN python3 /app/fedor_recipe_book/manage.py collectstatic --noinput
RUN python3 /app/fedor_recipe_book/manage.py migrate
RUN python3 /app/fedor_recipe_book/manage.py loaddata /app/fedor_recipe_book/recipe_book/fixtures/RecipeCategories.json

ARG DJANGO_PORT
EXPOSE $DJANGO_PORT

CMD ["python3", "/app/fedor_recipe_book/manage.py", "runserver", "0.0.0.0:8000"]