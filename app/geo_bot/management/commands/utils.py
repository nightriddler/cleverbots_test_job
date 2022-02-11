import logging

import requests
from geo_bot.models import Result, SearchArea, TelegramUser
from requests.exceptions import RequestException


def get_count_response(chat_id):
    """
    Количество поисковых запросов по chat_id.
    """
    message = []
    user = TelegramUser.objects.filter(user_id=chat_id).order_by("-id")
    if user:
        message += f"Вы совершили {user.count()} поисковых запросов.\n\n"
        message += [f"{response.result}\n" for response in user[:5]]
    else:
        message += ["Вы еще не сделали ни одного запроса."]
    return message


def get_addresses(location):
    """
    Получить ближайшие адреса по указанной локации.
    """
    response = get_response_geo(location)
    return response_processing(response)


def get_response_geo(location):
    """
    Поиск ближайшего адреса по указанной локации.
    """
    from django_tg_bot.settings import API_GEO_TOKEN

    try:
        response = requests.get(
            f"https://geocode-maps.yandex.ru/1.x?geocode={location}&apikey={API_GEO_TOKEN}&format=json&results=100",
        )
    except RequestException:
        logging.exception("Can not get response client.")
        return "Can not get response client."
    return response


def response_processing(response):
    """
    Выделение подходящих адресов из области поиска.
    """
    authorized_areas = [area.title.lower() for area in SearchArea.objects.all()]
    all_address = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    for address in all_address:
        area = address["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"][
            "Components"
        ]
        for component in area:
            if component["name"].lower() in authorized_areas:
                find_address = address["GeoObject"]["metaDataProperty"][
                    "GeocoderMetaData"
                ]["text"]
                return find_address
    # return "В доступных зонах поиска не найден адрес."


def save_db(location, result, chat_id):
    """
    Сохранение адреса в БД.
    """
    result, _ = Result.objects.get_or_create(query=location, result=result)
    TelegramUser.objects.get_or_create(user_id=chat_id, result=result)
