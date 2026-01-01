# Homework 8 for QAGURU 23

## Задание: Система рассылки писем в стиле ООП

### Описание

Объектно-ориентированная система отправки email сообщений с валидацией, статусами и логированием.

### Структура проекта

```
hw_8/
├── src/
│   ├── __init__.py
│   ├── status.py           # Status enum (DRAFT, READY, SENT, FAILED, INVALID)
│   ├── utils.py            # Утилита clean_text()
│   ├── email_address.py    # Класс EmailAddress с валидацией
│   ├── email.py            # Dataclass Email
│   └── service.py          # EmailService и LoggingEmailService
├── tests/
│   ├── __init__.py
│   └── test_email_system.py  # Тесты (21 тест)
├── example.py              # Демонстрационные примеры
├── pyproject.toml
└── README.md
```

### Основные компоненты

#### 1. Status (StrEnum)
Перечисление статусов письма:
- `DRAFT` - черновик
- `READY` - готово к отправке
- `SENT` - отправлено
- `FAILED` - ошибка отправки
- `INVALID` - невалидное письмо

#### 2. EmailAddress
Класс для работы с email адресами:
- Нормализация (нижний регистр, удаление пробелов)
- Валидация (наличие @, домены .com/.ru/.net)
- Маскирование (первые 2 символа + "***@" + домен)

```python
email = EmailAddress("Alice@Example.COM")
print(email.address)  # alice@example.com
print(email.masked)   # al***@example.com
```

#### 3. Email (dataclass)
Модель письма с полями:
- `subject` - тема
- `body` - текст
- `sender` - отправитель (EmailAddress)
- `recipients` - получатели (list[EmailAddress])
- `date` - дата отправки
- `short_body` - сокращённый текст
- `status` - статус

Методы:
- `prepare()` - подготовка к отправке (очистка, валидация)
- `clean_data()` - очистка текста
- `add_short_body(n=10)` - создание краткой версии
- `is_valid_fields()` - проверка полей

#### 4. EmailService
Сервис отправки писем:
- `send_email(email)` - отправка письма всем получателям
- Создаёт глубокую копию для каждого получателя
- Проставляет дату и статус
- Не изменяет исходное письмо

#### 5. LoggingEmailService
Расширенный сервис с логированием:
- Наследуется от EmailService
- Записывает информацию об отправке в файл

### Установка и запуск

```bash
# Установка зависимостей
poetry install

# Запуск тестов
poetry run pytest tests/ -v

# Проверка кода на PEP 8
poetry run flake8 src/ tests/

# Запуск демонстрационного примера
poetry run python example.py
```

### Примеры использования

#### Базовое использование

```python
from src.email import Email
from src.email_address import EmailAddress
from src.service import EmailService

# Создание адресов
sender = EmailAddress("alice@example.com")
recipients = [
    EmailAddress("bob@example.com"),
    EmailAddress("charlie@example.ru")
]

# Создание письма
email = Email(
    subject="Quarterly Report",
    body="Hello team,\n\tHere is the report.",
    sender=sender,
    recipients=recipients
)

# Подготовка
email.prepare()
print(email.status)  # Status.READY

# Отправка
service = EmailService()
sent_emails = service.send_email(email)
print(len(sent_emails))  # 2
```

#### Использование с логированием

```python
from src.service import LoggingEmailService
from src.status import Status

email.status = Status.READY
service = LoggingEmailService("send.log")
sent_emails = service.send_email(email)
# Информация записана в send.log
```

### Результаты тестирования

Все 21 тест успешно проходят:
- 6 тестов EmailAddress (валидация, нормализация, маскирование)
- 9 тестов Email (создание, очистка, подготовка)
- 4 теста EmailService (отправка одному/нескольким получателям)
- 2 теста LoggingEmailService (логирование)

### Соответствие требованиям

- Python 3.12+
- Код соответствует PEP 8 (макс. длина строки 90)
- Структура проекта корректна
- Мусорные файлы исключены через .gitignore
- Все компоненты покрыты тестами
- Документация и примеры включены
