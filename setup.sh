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

echo "Секретный код Django"
read SECRET_KEY

echo "Пароль DB"
read DB_PWD

echo "Имя пользователя от ящика gmail.com"
read MAIL_NAME

echo "Пароль от почты"
read MAIL_PWD

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
DJANGO_SECRET_KEY=$SECRET_KEY
EMAIL_HOST_USER=$MAIL_NAME
EMAIL_HOST_PASSWORD=$MAIL_PWD
MYSQL_PASSWORD=$DB_PWD
EOF

echo ".env файл успешно создан."
