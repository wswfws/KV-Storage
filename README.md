# KV-Storage

**KV-Storage** — это распределённое хранилище данных типа «ключ-значение», предоставляющее высокую надёжность,
масштабируемость и удобство работы. Система подходит для сценариев, где требуется надёжное хранение данных, репликация,
а также работа с большими объёмами информации.

---

## Возможности и особенности

- **Распределённая архитектура:** данные равномерно распределяются между узлами системы.
- **Сетевая реализация:** взаимодействие с хранилищем осуществляется через HTTP API.
- **Устойчивость к перезапуску:** данные сохраняются между запусками благодаря использованию файловой системы.
- **Поддержка больших данных:** работа с объёмами данных, не помещающимися в память.
- **Репликация данных:** резервное копирование для повышения отказоустойчивости.
- **Масштабируемость:** поддержка нескольких экземпляров хранилища для увеличения пропускной способности.
- **Обширное тестирование:** система протестирована на различных сценариях использования.
- **Эффективность:** оптимизированные алгоритмы поиска ключей и хранения данных.

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/wswfws/kv-storage.git
   ```
2. Установите зависимости:
   ```bash
   pip install -r req.txt
   ```
3. Запустите сервер:
   ```bash
   python server.py
   ```
4. Для тестирования локального клиента выполните:
   ```bash
   python client.py
   ```

---

# CLI Documentation for Key-Value System

This document describes how to use the Command-Line Interface (CLI) for interacting with the key-value system. The CLI
allows you to perform operations such as adding, retrieving, and clearing key-value pairs.

## Commands

### 1. `clear_key`

Clears the specified key from the system.

**Usage:**

```bash
python cli_interface.py clear_key <key>
```

**Arguments:**

- `<key>`: The key to clear.

**Example:**

```bash
python cli_interface.py clear_key my_key
```

### 2. `add_value`

Adds a value to a specified key.

**Usage:**

```bash
python cli_interface.py add_value <key> <value>
```

**Arguments:**

- `<key>`: The key to which the value should be added.
- `<value>`: The value to add.

**Example:**

```bash
python cli_interface.py add_value my_key my_value
```

### 3. `add_value_part`

Adds a partial value to a specified key. This operation is useful when constructing a value incrementally.

**Usage:**

```bash
python cli_interface.py add_value_part <key> <value>
```

**Arguments:**

- `<key>`: The key to which the partial value should be added.
- `<value>`: The partial value to add.

**Example:**

```bash
python cli_interface.py add_value_part my_key partial_value
```

### 4. `get_value`

Retrieves the value associated with a specified key.

**Usage:**

```bash
python cli_interface.py get_value <key>
```

**Arguments:**

- `<key>`: The key whose value should be retrieved.

**Example:**

```bash
python cli_interface.py get_value my_key
```

## Installation

Ensure you have Python installed on your system and the required dependencies for your module. Import necessary
functions from your key-value module.

## Running the CLI

To run the CLI, execute the script `cli_interface.py` with the desired command and arguments. Each command is designed
to handle a specific operation.

## Examples

### Add a value to a key

```bash
python cli_interface.py add_value test_key test_value
```

### Retrieve the value of a key

```bash
python cli_interface.py get_value test_key
```

### Clear a key

```bash
python cli_interface.py clear_key test_key
```

### Add a partial value to a key

```bash
python cli_interface.py add_value_part test_key part_value
```

---

## API

### `POST /add_value`

Добавление значения в хранилище.

**Параметры:**

- `key` (строка) — ключ.
- `value` (строка) — значение.
- `finish_value` (логическое) — завершён ли ввод значения.
- `user` (объект) — информация о пользователе.

**Пример запроса:**

```json
{
  "key": "example",
  "value": "some data",
  "finish_value": true,
  "user": {
    "user_id": "123",
    "password_hash": "abc123"
  }
}
```

---

### `POST /get_value`

Получение значения из хранилища.

**Параметры:**

- `key` (строка) — ключ.
- `user` (объект) — информация о пользователе.

**Пример запроса:**

```json
{
  "key": "example",
  "user": {
    "user_id": "123",
    "password_hash": "abc123"
  }
}
```

**Пример ответа:**

```json
{
  "key": "example",
  "value": [
    "some data"
  ]
}
```

---

### `POST /clear_key`

Удаление значения по ключу.

**Параметры:**

- `key` (строка) — ключ.
- `user` (объект) — информация о пользователе.

**Пример запроса:**

```json
{
  "key": "example",
  "user": {
    "user_id": "123",
    "password_hash": "abc123"
  }
}
```

---

## Тестирование

- Запуск автоматических тестов для локального тестирования:
  ```tests/start_test.py```

---

## Использование

```python
import asyncio
from client import add_value, get_value, clear_key


async def main():
    # Добавление значения
    await add_value("key", "value")

    # Получение значения
    value = await get_value("key")
    print("Value:", value)

    # Очистка ключа
    await clear_key("key")


asyncio.run(main())
```

---

## Дополнительно

- Поддержка частичных значений для сборки данных по частям.
- Автоматическая синхронизация данных между узлами.
- Валидация пользователей на каждом запросе.

---

## Авторы

- **Данил Еценков** 