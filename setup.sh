#!/bin/bash

echo "IP адрес сервера:"
read IP_ADDRESS

echo "Порт Django:"
read DJANGO_PORT

echo "SECRET_KEY Django"
read SECRET_KEY

echo "EMAIL_HOST"
read EMAIL_HOST

echo "EMAIL_PORT"
read EMAIL_PORT

echo "EMAIL_HOST_USER"
read EMAIL_HOST_USER

echo "EMAIL_HOST_PASSWORD"
read EMAIL_HOST_PASSWORD

echo "MYSQL_NAME "
read MYSQL_NAME

echo "MYSQL_USER"
read MYSQL_USER

echo "MYSQL_PASSWORD"
read MYSQL_PASSWORD

echo "MYSQL_HOST"
read MYSQL_HOST

cat <<EOF > .env
IP_ADDRESS=$IP_ADDRESS
DJANGO_PORT=$DJANGO_PORT

SECRET_KEY=$SECRET_KEY

EMAIL_HOST=$EMAIL_HOST
EMAIL_PORT=$EMAIL_PORT
EMAIL_HOST_USER=$EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

MYSQL_NAME=$MYSQL_NAME
MYSQL_USER=$MYSQL_USER
MYSQL_PASSWORD=$MYSQL_PASSWORD
MYSQL_HOST=$MYSQL_HOST
EOF

echo ".env создан"
