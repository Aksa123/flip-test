import unittest
import requests
import json
from helpers import generate_random_alphanumeric_string, generate_random_number, get_with_retry, retry_wrapper
from models import PokemonAbility, now_jkt
from datetime import datetime, timedelta, UTC
import requests
from time import sleep


class TestAPI(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)

    def test_length_random_alphanumeric(self):
        res = generate_random_alphanumeric_string(13)
        length = len(res)
        self.assertEqual(length, 13)

    def test_length_random_number(self):
        res = generate_random_number(7)
        length = len(res)
        self.assertEqual(length, 7)

    def test_retry_wrapper(self):
        retry_obj = retry_wrapper(3, 2)
        get_head = retry_obj(requests.head)
        res = get_head('https://pokeapi.co/api/v2/ability/150')
        self.assertEqual(res.status_code, 200)

    def test_default_now(self):
        item = PokemonAbility(
            raw_id=generate_random_alphanumeric_string(13),
            user_id=generate_random_number(7),
            pokemon_ability_id=999,
            effect='effect test desc',
            language={"name": "en", "url": "https://pokeapi.co/api/v2/language/9/"},
            short_effect='short effect test desc'   
        )
        
        dt = datetime.now(UTC) + timedelta(hours=7)
        dt_date = dt.date()
        dt_hour = dt.hour

        item_dt_date = item.created_at.date()
        item_dt_hour = item.created_at.hour
        
        self.assertEqual(dt_date, item_dt_date)
        self.assertEqual(dt_hour, item_dt_hour)