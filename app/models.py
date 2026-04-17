from peewee import PostgresqlDatabase, Model, AutoField, IntegerField, CharField, TextField, ForeignKeyField, DateTimeField
from settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from datetime import datetime, timedelta, timezone
from helpers import tz_jkt
import json


db = PostgresqlDatabase(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)

def get_now_callable_with_tz(tz: timezone):
    def inner():
        return datetime.now(tz)
    return inner

# Callable datetime.now with custom tz (Asia/Jakarta) for default DateTimeField
now_jkt = get_now_callable_with_tz(tz_jkt)

# Peewee doesn't have JSONField by default. Create one as a subclass of TextField + some validation
class JsonField(TextField):
    field_type = 'JSON'
    
    def adapt(self, value):
        if type(value) == dict:
            val = json.dumps(value)
            return val
        else:
            val = super().adapt(value)
            try:
                json.loads(val)
                return val
            except Exception as err:
                raise ValueError(f'Value is not JSON formattable: {value}')
    
    def python_value(self, value):
        if not value:
            return None
        val = json.loads(super().python_value(value))
        return val
    

class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class PokemonAbility(BaseModel):
    id = AutoField()                     # Primary key; auto-increment
    raw_id = CharField(max_length=13)
    user_id = IntegerField()
    pokemon_ability_id = IntegerField()
    effect = TextField()
    language = JsonField()
    short_effect = TextField(null=True)
    created_at = DateTimeField(default=now_jkt, formats=['%Y-%m-%d %H:%M:%S.%f%z'])


db.create_tables([PokemonAbility])