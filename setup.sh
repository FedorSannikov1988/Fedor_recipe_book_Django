#!/bin/bash

echo "Введите имя контейнера:"
read CONTAINER_NAME

echo "Введите IP адрес сервера:"
read IP_ADDRESS

echo "Введите порт для Django:"
read DJANGO_PORT

echo "Введите список разрешенных хостов (через запятую):"
read ALLOWED_HOSTS

echo "Хотите выключить режим отладки Django? (yes/no)"
read DEBUG_MODE

if [ "$DEBUG_MODE" == "yes" ]; then
    DJANGO_DEBUG="False"
else
    DJANGO_DEBUG="True"
fi

cat <<EOF > .env
CONTAINER_NAME=$CONTAINER_NAME
IP_ADDRESS=$IP_ADDRESS
DJANGO_PORT=$DJANGO_PORT
ALLOWED_HOSTS=$ALLOWED_HOSTS
DJANGO_DEBUG=$DJANGO_DEBUG
EOF

echo ".env файл успешно создан."
