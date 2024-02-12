# Api доски объявлений
## Регистация пользователя
### http://127.0.0.1:5000/register/
### Метод: POST
Данные:
  "name": String
  "email": String
  "password": String

## Аутентификация
### http://127.0.0.1:5000/login/
### Метод: POST
Данные:
  "email": String
  "password": String

## Создание объявлений
### http://127.0.0.1:5000/adv/
### Метод: POST
Данные:
  "title": String
  "description": String
### Метод: PATCH, DELETE
http://127.0.0.1:5000/adv/adv_id/