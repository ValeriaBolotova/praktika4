
# Encryption Service 2.0

## Описание

Этот сервис предоставляет REST API для шифрования и дешифрования данных с использованием методов Виженера и сдвига. API поддерживает работу с двумя алфавитами: английским и русским. Так же, есть интеграция базы данных SQLite 

## Установка

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/ValeriaBolotova/praktika4.git
    ```
2. Перейдите в папку проекта:
    ```bash
    cd <название папки проекта>
    ```
3. Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
4. Активируйте виртуальное окружение:

    - На Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - На macOS и Linux:
        ```bash
        source venv/bin/activate
        ```
5. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Запустите сервер:
```bash
python app.py
```

## Использование

### Добавление пользователя

**Endpoint:** `POST /users`

**Пример запроса:**
```json
{
    "login": "user1",
    "secret": "password"
}
```

**Пример ответа:**
```json
{
    "id": 1,
    "login": "user1",
    "secret": "password"
}
```

### Просмотр списка пользователей

**Endpoint:** `GET /users`

**Пример ответа:**
```json
[
    {
        "login": "user1",
        "id": 1
    }
]
```

### Удаление пользователя

**Endpoint:** `DELETE /users/<user_id>`

**Пример ответа:**
```json
{
    "status": "deleted"
}
```

### Просмотр методов шифрования

**Endpoint:** `GET /methods`

**Пример ответа:**
```json
[
    {
        "id": 1,
        "name": "vigenere",
        "caption": "Vigenere Cipher",
        "params": {"key": "str"},
        "description": "Шифрование методом Виженера"
    },
    {
        "id": 2,
        "name": "shift",
        "caption": "Shift Cipher",
        "params": {"shift": "int"},
        "description": "Шифрование методом сдвига"
    }
]
```

### Создание сессии шифрования/дешифрования

**Endpoint:** `POST /sessions`

**Пример запроса для шифрования методом Виженера (EN):**
```json
{
    "user_id": 1,
    "method_id": 1,
    "text": "HELLO",
    "params": {"key": "KEY"},
    "operation": "encrypt",
    "language": "en"
}
```

**Пример запроса для шифрования методом Виженера (RU):**
```json
{
    "user_id": 1,
    "method_id": 1,
    "text": "ПРИВЕТ",
    "params": {"key": "КЛЮЧ"},
    "operation": "encrypt",
    "language": "ru"
}
```

**Пример запроса для дешифрования методом Виженера (EN):**
```json
{
    "user_id": 1,
    "method_id": 1,
    "text": "RI9VS",
    "params": {"key": "KEY"},
    "operation": "decrypt",
    "language": "en"
}
```

**Пример запроса для дешифрования методом Виженера (RU):**
```json
{
    "user_id": 1,
    "method_id": 1,
    "text": "ЪЬ7ЩПЮ",
    "params": {"key": "КЛЮЧ"},
    "operation": "decrypt",
    "language": "ru"
}
```

**Пример запроса для шифрования методом сдвига (EN):**
```json
{
    "user_id": 1,
    "method_id": 2,
    "text": "HELLO",
    "params": {"shift": 3},
    "operation": "encrypt",
    "language": "en"
}
```

**Пример запроса для шифрования методом сдвига (RU):**
```json
{
    "user_id": 1,
    "method_id": 2,
    "text": "ПРИВЕТ",
    "params": {"shift": 3},
    "operation": "encrypt",
    "language": "ru"
}
```

**Пример запроса для дешифрования методом сдвига (EN):**
```json
{
    "user_id": 1,
    "method_id": 2,
    "text": "KHOOR",
    "params": {"shift": 3},
    "operation": "decrypt",
    "language": "en"
}
```

**Пример запроса для дешифрования методом сдвига (RU):**
```json
{
    "user_id": 1,
    "method_id": 2,
    "text": "ТУЛЕЗХ",
    "params": {"shift": 3},
    "operation": "decrypt",
    "language": "ru"
}
```

**Пример ответа:**
```json
{
    "id": 1,
    "user_id": 1,
    "method_id": 1,
    "data_in": "HELLO",
    "params": {"key": "KEY"},
    "data_out": "RI9VS",
    "status": "completed",
    "created_at": "2024-06-21T12:34:56.789123",
    "time_out": 0.001234
}
```

### Просмотр списка сессий

**Endpoint:** `GET /sessions`

**Пример ответа:**
```json
[
    {
        "id": 1,
        "user_id": 1,
        "method_id": 1,
        "data_in": "HELLO",
        "params": {"key": "KEY"},
        "data_out": "RI9VS",
        "status": "completed",
        "created_at": "2024-06-21T12:34:56.789123",
        "time_out": 0.001234
    }
]
```

### Удаление сессии

**Endpoint:** `DELETE /sessions/<session_id>`

**Пример запроса:**
```json
{
    "secret": "password"
}
```

**Пример ответа:**
```json
{
    "status": "deleted"
}
```

### Взлом шифра

**Endpoint:** `POST /break`

**Описание:** Этот endpoint позволяет взломать шифр сдвига, перебирая все возможные сдвиги и возвращая все возможные результаты.

**Пример запроса:**
```json
{
    "method_id": 2,
    "text": "KHOOR",
    "language": "en"
}
```

**Пример ответа:**
```json
{
    "possible_texts": [
        "KHOOR",
        "JGNNQ",
        "IFMMP",
        "HELLO",
        "GDKKN",
        "FCJJM",
        "EBIIL",
        "DAHHK",
        "C)GGJ",
        "B.FFI",
        "A.EEH",
        ").DDG",
        ".(CCF",
        ".,BBE",
        "..AAD",
        "(9))C",
        ",8..B",
        ".7..A",
        "96..)",
        "85((.",
        "74,,.",
        "63...",
        "5299(",
        "4188,",
        "3077.",
        "2Z669",
        "1Y558",
        "0X447",
        "ZW336",
        "YV225",
        "XU114",
        "WT003",
        "VSZZ2",
        "URYY1",
        "TQXX0",
        "SPWWZ",
        "ROVVY",
        "QNUUX",
        "PMTTW",
        "OLSSV",
        "NKRRU",
        "MJQQT",
        "LIPPS"
    ]
}
```
