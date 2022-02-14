from django.test import TestCase

import django_tg_bot.settings
from geo_bot.management.commands.utils.seacrh import (
    get_addresses,
    get_response_geo,
    response_processing,
    save_db,
)
from geo_bot.models import SearchArea, TelegramUser


class SearchBotTest(TestCase):
    search = "Москва"
    user_id = "12345678"

    def setUp(self):
        SearchArea.objects.create(title=self.search)

    def test_get_response_geo(self):
        """
        Тест получения ответа по запросу поиска до ближайшего адреса указанной локации.
        """
        self.assertTrue(
            "API_GEO_TOKEN" in dir(django_tg_bot.settings),
            "Укажите в settings API Geo токен.",
        )
        response = get_response_geo("Красная площадь")
        self.assertEqual(response.status_code, 200)

    def test_response_processing(self):
        """
        Тест на выделение подходящих адресов из области поиска, сохранение их в БД и выдача результата.
        """
        response = get_response_geo("Красная площадь")
        location = response_processing(response)

        self.assertTrue(
            self.search in location
        ), f"{self.search} не найдена. Проверьте находится ли {self.search}в базе."

        SearchArea.objects.filter(title=self.search).delete()
        area = "Орловская область"
        SearchArea.objects.create(title=area)

        query = "Красная площадь"
        location = get_addresses(query)
        save_db(location, query, self.user_id)
        count_query = TelegramUser.objects.filter(user_id=self.user_id).count()

        self.assertTrue(
            area in location
        ), f"{self.search} не найдена. Проверьте находится ли {self.search}в базе."
        self.assertEqual(
            count_query, 1, "Проверьте сколько областей поиска добавлено в БД."
        )

        query = "Орел"
        location = get_addresses(query)
        save_db(location, query, self.user_id)
        count_query = TelegramUser.objects.filter(user_id=self.user_id).count()

        self.assertEqual(
            count_query, 2, "Проверьте сколько областей поиска добавлено в БД."
        )
