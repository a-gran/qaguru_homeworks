from datetime import date



# Часть А. Функции
'''
Создайте набор функций для обработки информации о письме из HW4.
Каждая функция должна выполнять ровно одно действие и возвращать результат.
Аргументы и возвращаемые значения должны быть понятны по названию функции.

email = {
    "subject": "Quarterly Report",
    "from": "Alice.Cooper@Company. ",
    "to": " bob_smith@Gmail.com ",
    "body": "Hello Bob,\n\tHere is the quarterly report.\n\tPlease review and let me know your feedback.\n\nBest,\nAlice",
}
'''

# 1. Нормализация email адресов
def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()


# 2. Сокращенная версия тела письма
def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    email["short_body"] = email["body"][:10] + "..."
    return email


# 3. Очистка текста письма
def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace('\n', ' ').replace('\t', ' ')


# 4. Формирование итогового текста письма
def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    clean_body = clean_body_text(email["body"])

    return f"""Кому: {email['to']}, от {email['from']}
            Тема: {email['subject']}, дата {email['date']}
            {clean_body}"""


# 5. Проверка пустоты темы и тела
def check_empty_fields(subject: str, body:str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = not subject.strip()
    is_body_empty = not body.strip()

    return (is_subject_empty, is_body_empty)


# 6. Маска email отправителя
def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return login[:2] + "***@" + domain


# 7. Создать функцию которая проверит корректности email адресов. Адрес считается корректным, если:
# содержит символ @;
# оканчивается на один из доменов: .com, .ru, .net.
# Список emails для проверки работы функции
test_emails = [
    # Корректные адреса
    "user@gmail.com",
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    "default@study.com",
    " hello@corp.ru  ",
    "user@site.NET",
    "user@domain.coM",
    "user.name@domain.ru",
    "usergmail.com",
    "user@domain",
    "user@domain.org",
    "@mail.ru",
    "name@.com",
    "name@domain.comm",
    "",
    "   ",
]

def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    correct_emails = []
    valid_domains = ('.com', '.ru', '.net')

    for email in email_list:
        # Очищаем от пробелов и приводим к нижнему регистру
        cleaned_email = email.strip().lower()

        # Базовые проверки
        if not cleaned_email or '@' not in cleaned_email:
            continue

        # Разделяем на логин и домен
        parts = cleaned_email.split('@')

        # Должен быть ровно один символ @
        if len(parts) != 2:
            continue

        login, domain = parts

        # Логин не должен быть пустым
        if not login:
            continue

        # Домен должен заканчиваться на валидные зоны
        if not domain.endswith(valid_domains):
            continue

        # Проверяем, что между @ и доменной зоной есть символы
        # Убираем доменную зону и проверяем остаток
        for zone in valid_domains:
            if domain.endswith(zone):
                domain_without_zone = domain[:-len(zone)]
                if domain_without_zone:  # Должно быть что-то перед .com/.ru/.net
                    correct_emails.append(cleaned_email)
                break

    return correct_emails


# 8. Создание словаря письма
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {
        'sender': sender,
        'recipient': recipient,
        'subject': subject,
        'body': body
    }


# 9. Добавление даты отправки
def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = date.today().isoformat()
    return email


# 10. Получение логина и домена
def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    return tuple(address.split('@'))


# Часть B. Отправка письма
# Создать функцию отправки письма с базовой валидацией адресов и логикой выбора отправителя recipient

'''
Требования к функции
Функция sender_email принимает 3 позиционных аргумента recipient_list — emails получателя,
subject — заголовок письма, message — текст письма и один обязательно именованный sender="default@study.com".

Внутри функции реализовать строго в указанном порядке:
- Проверить, что recipient_list не пустой.
- Проверить корректность email отправителя и получателей через get_correct_email().
- Проверить пустоту темы и тела письма через check_empty_fields(). Если одно из них пустое — вернуть пустой список.
- Исключить отправку самому себе: пройти по каждому элементу recipient_list в цикле for, если адрес совпадает с sender, удалить его из списка.
- Нормализовать: subject и body → с помощью clean_body_text() recipient_list и sender → с помощью normalize_addresses()
- Создать письмо для каждого получателя функцией create_email().
- Добавить дату отправки с помощью add_send_date().
- Замаскировать email отправителя с помощью extract_login_domain() и mask_sender_email().
- Сохранить короткую версию в email["short_body"].
- Сформировать итоговый текст письма функцией build_sent_text().
- Вернуть итоговый список писем.

Пример готового dict email:
[
    {
        'recipient': 'admin@company.ru',
        'sender': 'default@study.com',
        'subject': 'Hello!',
        'date': '2025-11-04',
        'body': 'Привет, коллега!',
        'masked_sender': 'de***@study.com',
        'short_body': 'Привет, ко...',
        'sent_text': 'Кому: admin@company.ru, от default@study.com\nТема: Hello!, дата 2025-11-04\nПривет, ко...'
    },
    ...
]

Результат: Вывод готово списка писем функцией
[
    Кому: {masked to}, от {masked from}
    Тема: {subject}, дата {date}
    {short_clean_body}
      ] ...
'''

def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    # Проверить, что recipient_list не пустой
    if not recipient_list:
        return []

    # Проверить корректность email отправителя и получателей через get_correct_email()
    valid_recipients = get_correct_email(recipient_list)
    valid_sender_list = get_correct_email([sender])

    if not valid_sender_list or not valid_recipients:
        return []

    sender_normalized = valid_sender_list[0]

    # Проверить пустоту темы и тела письма через check_empty_fields()
    is_subject_empty, is_body_empty = check_empty_fields(subject, message)
    if is_subject_empty or is_body_empty:
        return []

    # Исключить отправку самому себе
    recipients_filtered = [r for r in valid_recipients if r != sender_normalized]

    if not recipients_filtered:
        return []

    # Нормализовать: subject и body → clean_body_text()
    # recipient_list и sender уже нормализованы через get_correct_email()
    subject_clean = clean_body_text(subject)
    body_clean = clean_body_text(message)

    # Создать письмо для каждого получателя
    emails = []
    for recipient in recipients_filtered:
        # Создать письмо функцией create_email()
        email = create_email(
            sender=sender_normalized,
            recipient=recipient,
            subject=subject_clean,
            body=body_clean
        )

        # Добавить дату отправки с помощью add_send_date()
        email = add_send_date(email)

        # Замаскировать email отправителя
        login, domain = extract_login_domain(sender_normalized)
        email['masked_sender'] = mask_sender_email(login, domain)

        # Сохранить короткую версию в email["short_body"]
        email = add_short_body(email)

        # Сформировать итоговый текст письма
        # Используем short_body согласно примеру результата
        email['sent_text'] = f"""Кому: {email['recipient']}, от {email['sender']}
                                Тема: {email['subject']}, дата {email['date']}
                                {email['short_body']}"""

        emails.append(email)

    # Вернуть итоговый список писем
    return emails




