# CW5

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
Задача: игра с веб-интерфейсом о битве героев в стиле олдскульных браузерных игор.

Добавлено мной: 
- сохранение результатов игр в бд
- докер и докер-компоуз для автоматический сборки приложения
- git actions для деплоя изменений на сервер
- добавил еще одного персонажа с 'другим' умением

Так же считаю предложенные характеристики героев и правила битвы сильно разбалансированными. Битва идёт очень долго. Стамина почти никогда не кончается. Произвёл ребалансировку на свой вкус.
И мне не очень понравилась идея хранить тип героя в датаклассах. Не уверен, как сделать было бы наиболее хорошо, но пока сделал просто наследованием от базового класса. Плюс фабричный метод для сборки объекта героя.
