# SocialMediaAPI
## REST API для работы "социальной сети"
<image src="https://graphicsland.ru/wp-content/uploads/social_icons_circle_color.png" alt="картинка" width="410" height="270">

### Используемый стек технологий
* Python 3.11
* FastAPI
* Pydantic
* База данных
    + PostgreSQL
    + SQLAlchemy
    + Alembic
* Pytest
* Redis
* Разработка и Инфроструктура
    + Git
    + Docker Compose
    + Nginx

### Описание возможностей API
- зарегистрировать нового пользователя
- отправить одному пользователю заявку в друзья другому
- принять/отклонить пользователю заявку в друзья от другого
пользователя
- посмотреть пользователю список своих исходящих и входящих заявок
в друзья
- посмотреть пользователю список своих друзей
- получить пользователю статус дружбы с каким-то другим
пользователем (нет ничего / есть исходящая заявка / есть входящая
заявка / уже друзья)
- удалить пользователю другого пользователя из своих друзей
- если пользователь1 отправляет заявку в друзья пользователю2, а
пользователь2 отправляет заявку пользователю1, то они автоматически
становятся друзьями

## Документация (с возможностью делать запросы)
http://zkramorev.ru/docs
## Установка и запуск на локальной машине
### **С** использованием Docker Compose
1. `git clone git@github.com:zkramorev/SocialMediaAPI.git`
2. ```cd SocialMediaAPI```
3. ```docker compose build```
4. ```docker compose up```
5. Переходим на [http://127.0.0.1/docs](http://127.0.0.1/docs) 
### **Без** использования Docker Compose
1. ```git clone git@github.com:zkramorev/SocialMediaAPI.git```
2. ```cd SocialMediaAPI```
3. ```python3 -m venv venv ```
4. ```. venv/bin/activate```
5. ```pip install -r requirements.txt```
6. ```uvicorn app.main:app```
7. Переходим на [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)