import requests
import pymorphy2
from isoweek import Week
import re
# from peewee import *
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import Counter
import sys


# class Articles(Model):
#     header = CharField()
#     article_date = DateField()
#     article_link = CharField()
#     text_of_article = TextField()
#     number_of_week = IntegerField()
#
#     class Meta:
#         database = SqliteDatabase('articles.db')


def get_page(pages):
    url = "https://habr.com/all/all/page{}/"
    urls = []
    for page_number in range(1, pages+1):
        urls.append(requests.get(url.format(page_number)).text)
    return urls


def is_noun(words):
    """Привет, кот пошел налево в дом -> ["кот","дом"] """
    nouns_list = []
    words = re.split('\W+', words)
    morph = pymorphy2.MorphAnalyzer()
    count = 0
    for word in words:
        count += 1
        # print("Обработано {} слов из {}".format(count, len(words)))
        if word:
            info = morph.parse(word)
            if "NOUN" in info[0][1]:
                nouns_list.append(info[0].normal_form)
    return nouns_list


def take_number_of_week(data):
    # 24.04.2017 -> 17(Номер недели)
    data = data.replace('.', ',').split(',')
    number_of_week = datetime(int(data[2]), int(data[1]), int(data[0]))
    return number_of_week.isocalendar()[1]


def formatting_date(str_date):
    """ вчера в 17.01" -> day-1. month .year
     сегодня в 17.01" -> day. month .year
     25 апреля в 23:34 -> 25.04. +year !!!"""
    if str_date.startswith('вчера'):
        return (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
    elif str_date.startswith('сегодня'):
        return datetime.now().strftime('%d.%m.%Y')
    else:
        months = {"января": '01',
                  "февраля": '02',
                  "марта": '03',
                  "апреля": '04',
                  "мая": '05',
                  "июня": '06',
                  "июля": '07',
                  "августа": '08',
                  "сентября": '09',
                  "октября": '10',
                  "ноября": '11',
                  "декабря": '12'}
        str_date = str_date.replace(' ', '.')
        for month in months.keys():
            if str_date.find(month) > 0:
                str_date = str_date.replace(month, months[month])[:5]
                return str_date + datetime.now().strftime('.%Y')


def parsing_file(count_pages):
    article_information = []
    for page in get_page(count_pages):
        file_content = BeautifulSoup(page, "lxml")
        articles = file_content.find_all("article")
        for article in articles:
            article_header = article.find("h2")
            date_of_publication = article.find("span", {"class": "post__time"}).contents[0]
            article_link = article_header.find("a")
            article_information.append(dict(header=article_header.contents[1].contents[0],
                                            article_date=formatting_date(date_of_publication),
                                            article_link=article_link["href"]))
    return article_information


# def create_db_item(item):
#     Articles.get_or_create(header=item["header"],
#                            article_date=item["article_date"],
#                            article_link=item["article_link"],
#                            text_of_article=item["text_of_article"],
#                            number_of_week=item["number_of_week"])
#
#     return None


def get_text_of_article(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    text_of_article = soup.find("div", {"class": "post__text"})
    return text_of_article.get_text()


def get_all_text_on_the_week(week_number, all_articles):
    all_text = ''
    for article in all_articles:
        if week_number == article["number_of_week"]:
            all_text += article["text_of_article"]
    return all_text


def get_all_text_in_all_weeks(articles):
    """ number of week : text
    17:asdasdasdadaads, 13:qweasdsadasdsa"""
    weeks = []
    text_and_number_week = {}
    for article in articles:
        weeks.append(article["number_of_week"])
    unic_weeks = list(set(weeks))
    for week in unic_weeks:
        text_and_number_week[week] = get_all_text_on_the_week(week, articles)
    return text_and_number_week


def string_description_week_from_week_number(week_number):
    now_year = datetime.now().year
    week_obj = Week(now_year, week_number)
    return "Неделя с {} по {}".format(week_obj.monday(), week_obj.sunday())


def main():
    try:
        number_of_pages = int(sys.argv[1])
    except IndexError:
        number_of_pages = int(input("Введите количество страниц для парсинга"))
    # Articles.create_table()
    finally_result = {}
    values = parsing_file(number_of_pages)
    for elem in values:
        text = get_text_of_article(link=elem['article_link']).replace("\r", ' ').replace("\n", ' ')
        elem['text_of_article'] = text
        elem['number_of_week'] = take_number_of_week(elem['article_date'])
        # create_db_item(elem)
        print("Загружена статья: ", elem["header"])
    print("Количество просмотренных страниц: {}\nКоличество загруженных статей: {}"
          .format(number_of_pages, len(values)))
    print('\n', '*' * 60)
    print("---------------------------Ожидаем---------------------------")
    all_text_for_week = get_all_text_in_all_weeks(values)
    for index, elem in all_text_for_week.items():
        three_most_commons_nouns = Counter(is_noun(elem)).most_common(3)
        finally_result[string_description_week_from_week_number(index)] = three_most_commons_nouns
    for key, value in finally_result.items():
        k = 0
        print('*'*60)
        print(key)
        for i in value:
            k += 1
            print("\n{}){}".format(k, i))
        print('*' * 60)


if __name__ == '__main__':
    main()
