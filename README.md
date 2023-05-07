# Проект Foodgram 
![workflow status](https://github.com/AndreyDolgodvorov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание
На сайте «Продуктовый помощник» пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяетт пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 



## Запуск проекта на удаленном сервере
1. Клонировать репозиторий на сервер:
```
git clone git@github.com:AndreyDolgodvorov/foodgram-project-react.git
```
2. Установить на сервер Docker и Docker Compose:
```
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```
3. Перейти в каталог "infra" и создать файл .env по шаблону:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='уникальный_секретный_ключ'
```
4. Запустить контейнеры:
```
docker-compose up -d --build
```
5. Создать и применить файлы миграций, подгрузить статику, импортировать ингридиенты из CSV-файла:
```
sudo docker-compose exec -T backend python manage.py makemigrations
sudo docker-compose exec -T backend python manage.py migrate
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
sudo docker-compose exec -T backend python manage.py import_from_csv
```
6. При необходимости заполнить БД тестовыми данными:
```
sudo docker-compose exec -T backend python manage.py loaddata fixtures.json
```

## Пример
Проект запущен и доступен по адресу: [food-gram.zapto.org](http://food-gram.zapto.org/recipes)

___email/пароль тестовых пользователей:___\
_vpupkin@yandex.ru/pupkin_\
_emedvedev@yandex.ru/medvedev_\
_avolkova@yandex.ru/volkova_\

### Админ зона
http://food-gram.zapto.org/admin

_логин/пароль superuser: admin/admin_

<<<<<<< HEAD
=======
___email/пароль тестовых пользователей:___
_vpupkin@yandex.ru/pupkin_

_emedvedev@yandex.ru/medvedev_

_avolkova@yandex.ru/volkova_
>>>>>>> 245d93c95ee9fdcc80ce480fcb772d50c884a957

Проект запущен и доступен по адресу: food-gram.zapto.org

## Технологии
* Python 3.7
* Django 2.2.16
* DjangoRestFramework 3.12.4
* PostgreSQL 13.0
* Gunicorn 20.0.4
* Nginx 1.21.3


## Автор backend:
* Андрей Долгодворов
