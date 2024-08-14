Translation: RU | [EN](./README.md)

<!-- TOC -->
* [Описание](#описание)
* [Запуск](#запуск)
  * [Генерация приватного ключа](#генерация-приватного-ключа)
  * [Конфигурация](#конфигурация)
  * [Запустить](#запустить)
* [Возможности](#возможности)
  * [Задачи](#задачи)
  * [Списки](#списки)
* [Общий доступ](#общий-доступ)
  * [Публичные списки](#публичные-списки)
  * [Коллаборация](#коллаборация)
  * [Частные случаи](#частные-случаи)
    * [Перемещение задачи в другой список](#перемещение-задачи-в-другой-список)
    * [Редактирование задачи](#редактирование-задачи)
<!-- TOC -->


# Описание

Это приложение для управления заметками.
Кроме обычной работы с заметками приложение позволяет
создавать общий доступ к спискам задач и задачам внутри.

# Запуск

## Генерация приватного ключа

Для работы JWT нужно сгенерировать RSA ключ в формате PEM

```
openssl genrsa -out key_name.pem 2048
```

Не забудьте необходимые права на чтение.

## Конфигурация

Конфигурация осуществляется с помощью переменных окружения или
с помощью .env файла. Пример настроек можно посмотреть в [.env.example](./.env.example)

Подробное описание настроек можно прочитать [здесь](./docs/ru/CONFIG.md).


## Запуск

Перед запуском обязательно установите `API_PORT` и `AUTH_PRIVATE_KEY_PATH`

```
docker compose up
```

# Возможности

## Задачи

1. Создание
2. Поиск
3. Удаление
4. Пометка завершённым
5. Поиск по фильтрам
6. Складывание в списки

## Списки

1. Создание
2. Удаление
3. Поиск
4. Общий доступ (подробнее ниже)

# Общий доступ

## Публичные списки

Задачи из публичного списка может видеть каждый пользователь,
но изменять что-либо в таких списках может только создатель и
те у кого есть доступ для обновления.

Публичные списки нельзя найти в поиске если нет общего доступа.

## Коллаборация

Коллабораторы могут иметь возможность изменять состояние ресурсов.
Для ограничения их возможности существуют правила.
Если пользователю не предоставлено ни одно из правил, то для него будет режим только чтения.

На данный момент доступные правила:

- update_tasks - Позволяет обновлять существующие задачи.
- manage_tasks - Позволяет удалять/добавлять задачи.

## Частные случаи

### Перемещение задачи в другой список

Пользователь выполняющий перенос должен иметь права: `manage_tasks` в обоих
списках, `update_task` в изначальном списке.
У создателя задачи должно быть хотя бы право на чтение.

### Редактирование задачи

Пользователь может изменять свои задачи, если у него право на чтение.
Это утверждение верно так же для случаев, когда:

- У пользователя есть только право `manage_tasks`
- Пользователю ограничили доступ на редактирование