#!/bin/bash

echo "Имя контейнера:"
read CONTAINER_NAME

echo "IP адрес сервера:"
read IP_ADDRESS

echo "Порт Django:"
read DJANGO_PORT

echo "Введите список разрешенных хостов (через запятую):"
read ALLOWED_HOSTS

echo "Хотите выключить режим отладки Django? (yes/no)"
read DEBUG_MODE

echo "SECRET_KEY Django"
read SECRET_KEY

echo "EMAIL_HOST Django"
read EMAIL_HOST

echo "EMAIL_PORT Django"
read EMAIL_PORT

echo "EMAIL_HOST_USER Django"
read EMAIL_HOST_USER

echo "EMAIL_HOST_PASSWORD Django"
read EMAIL_HOST_PASSWORD

echo "MYSQL_PASSWORD Django"
read MYSQL_PASSWORD

cat <<EOF > .env
CONTAINER_NAME=$CONTAINER_NAME
IP_ADDRESS=$IP_ADDRESS
DJANGO_PORT=$DJANGO_PORT
ALLOWED_HOSTS=$ALLOWED_HOSTS

SECRET_KEY=$SECRET_KEY

EMAIL_HOST=$EMAIL_HOST
EMAIL_PORT=$EMAIL_PORT
EMAIL_HOST_USER=$EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

MYSQL_PASSWORD=$MYSQL_PASSWORD
EOF

echo ".env создан."
