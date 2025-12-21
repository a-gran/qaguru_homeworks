import re
from datetime import datetime
from pprint import pprint

# 1. Создайте словарь email, содержащий следующие поля:
# "subject" (тема письма), "from" (адрес отправителя), "to" (адрес получателя), "body" (текст письма).
email = {
    "subject": "Quarterly Report",
    "from": "Alice.Cooper@Company. ",
    "to": " bob_smith@Gmail.com ",
    "body": "Hello Bob,\n\tHere is the quarterly report.\n\tPlease review and let me know your feedback.\n\nBest,\nAlice",
}


# 2. Добавьте дату отправки: создайте переменную send_date как текущую дату в формате YYYY-MM-DD и запишите её в email["date"].
send_date = datetime.now().strftime("%Y-%m-%d")
email["date"] = send_date


# 3. Нормализуйте e-mail адреса отправителя и получателя: приведите к нижнему регистру и уберите пробелы по краям.
# Запишите обратно в email["from"] и email["to"].
email["from"] = email["from"].strip().lower()
email["to"] = email["to"].strip().lower()


# 4. Извлеките логин и домен отправителя в две переменные login и domain.
login = email["from"].split("@")[0]
domain = email["from"].split("@")[1]


# 5. Создайте сокращённую версию текста: возьмите первые 10 символов email["body"] и добавьте многоточие "...".
# Сохраните в новый ключ словаря: email["short_body"].
email["short_body"] = (
    email["body"].replace("\t", " ").replace("\n", " ").replace("  ", " ")[:10] + "..."
)


# 6. Списки доменов: создайте список личных доменов и список корпоративных доменов
# с учетом того что там должны быть только уникальные значения
personal_domains = [
    "gmail.com",
    "list.ru",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "icloud.com",
    "yandex.ru",
    "mail.ru",
    "list.ru",
    "bk.ru",
    "inbox.ru",
]
company_domains = [
    "company.ru",
    "corporation.com",
    "university.edu",
    "organization.org",
    "company.ru",
    "business.net",
]

personal_domains = set(personal_domains)
company_domains = set(company_domains)


# 7. Проверьте что в списке личных и корпоративных доменов нет пересечений:
# ни один домен не должен входить в оба списка одновременно.
duplicates = company_domains & personal_domains


# 8.  Проверьте «корпоративность» отправителя: создайте булеву переменную is_corporate, равную результату проверки вхождения домена отправителя в список корпоративных доменов.
is_corporate = domain in company_domains


# 9. Соберите «чистый» текст сообщения без табов и переводов строк: замените "\t" и "\n" на пробел.
# Сохраните в email["clean_body"].
# использовал модуль re для регулярных выражений
email["clean_body"] = re.sub(r"\s+", " ", email["body"])


# 10. Сформируйте текст отправленного письма многострочной f-строкой и сохраните в email["sent_text"]:
# Кому: {получатель}, от {отправитель} Тема: {тема письма}, дата {дата} {чистый текст сообщения}
email["sent_text"] = (
    f"\nКому: {email['to']},\nOт {email['from']}\nТема: {email['subject']},\nДата {email['date']}\n{email['clean_body']}"
)


# 11. Рассчитайте количество страниц печати для email["sent_text"], если на 1 страницу помещается 500 символов.
# Сохраните результат в переменную pages. Значение должно быть округленно в большую сторону.
pages = (len(email["sent_text"]) + 499) // 500


# 12. Проверьте пустоту темы и тела письма: создайте переменные is_subject_empty, is_body_empty в котором будет хранится что тема письма содержит данные.
is_subject_empty = not email["subject"].strip()
is_body_empty = not email["body"].strip()


# 13. Создайте «маску» e-mail отправителя: первые 2 символа логина + "***@" + домен.
# Запишите в email["masked_from"].
email["masked_from"] = login[:2] + "***@" + domain


# 14. Удалите из списка личных доменов значения "list.ru" и "bk.ru".
domains_to_remove = {"list.ru", "bk.ru"}

for domain in domains_to_remove:
    if domain in personal_domains:
        personal_domains.remove(domain)


print("\t")
print("email['from']: ", email["from"])
print("email['to']: ", email["to"])
print(f"Логин: {login}")
print(f"Домен: {domain}")
print("email['short_body']: ", email["short_body"])
print("\t")
print(f"Личные домены: {personal_domains}")
print("\t")
print(f"Корпоративные домены: {company_domains}")
print("\t")
print(f"Есть пересечения: {duplicates}" if duplicates else "Пересечений нет")
print("is_corporate: ", is_corporate)
print("\t")
print("email['clean_body']: ", email["clean_body"])
print("\t")
print('email["sent_text"]: ', email["sent_text"])
print("\t")
print(f"Количество страниц для печати: {pages}")
print("is_subject_empty: ", is_subject_empty)
print("is_body_empty: ", is_body_empty)
print("email['masked_from']: ", email["masked_from"])
print("\t")
pprint(email, width=300)
