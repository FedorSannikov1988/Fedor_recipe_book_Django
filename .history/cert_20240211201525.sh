#!/bin/bash

# Запускаем Certbot в контейнере для получения сертификатов
docker exec -it certbot-container certbot certonly --webroot --webroot-path /var/www/html -d yourdomain.com

# Проверяем, успешно ли был получен сертификат
if [ $? -eq 0 ]; then
    echo "Сертификаты успешно получены."

    # Копируем сертификаты в папку, указанную в конфигурационном файле NGINX
    docker cp certbot-container:/etc/letsencrypt/live/yourdomain.com/fullchain.pem /path/to/nginx/certs/server.crt
    docker cp certbot-container:/etc/letsencrypt/live/yourdomain.com/privkey.pem /path/to/nginx/certs/server.key

    # Перезапускаем контейнер с NGINX для применения новых сертификатов
    docker restart nginx-container

    echo "Сертификаты успешно скопированы и применены в NGINX."
else
    echo "Ошибка при получении сертификатов. Проверьте логи Certbot."
fi
