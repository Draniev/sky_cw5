# CW5

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Задача: игра с веб-интерфейсом о битве героев в стиле олдскульных браузерных игор.

Добавлено мной: 
- сохранение результатов игр в бд
- докер и докер-компоуз для автоматический сборки приложения
- git actions для деплоя изменений на сервер
- добавил еще одного персонажа с 'другим' умением
- поменял правила игры на свой вкус

Посчитал предложенные в задании характеристики героев и правила битвы сильно разбалансированными. 
Битва идёт очень долго. Стамина почти никогда не кончается. Произвёл ребалансировку на свой вкус. 
Идеальной балансировки все равно не получилось, но уже лучше. Впрочем, сейчас всё сильно зависит от оружия и брони. 
Священник вполне может завалить война, если первый с топориком или ножом а второй с ладошками. Но первый уставать
будет. И бой затянется %).

И, мне не очень понравилась идея хранить тип героя в датаклассах. И делать отдельные классы для пользователя и NPS тоже не понравилось. И еще что-то не понравилось. Так что игра получилась не совсем как по ТЗ, но, не думаю что это важно :).
