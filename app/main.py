import requests
import json
from fastapi import FastAPI
from models import PokemonAbility
from helpers import generate_random_alphanumeric_string, generate_random_number, get_with_retry
from loggers import logger
from pydantic import BaseModel

app = FastAPI()

class ResponseObject(BaseModel):
    success: bool
    msg: str
    error: str | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/pokemon-ability/{id}")
async def pokemon_ability(id: int):
    res = get_with_retry(f'https://pokeapi.co/api/v2/ability/{id}')
    if res.status_code == 404:
        msg = f'Ability id {id} not found'
        logger.info(msg)
        return ResponseObject(success=False, msg=msg, error='404 data not found')
    
    content = json.loads(res.content.decode())
    effect_entries = content['effect_entries']
    pokemon_list = [i['pokemon']['name'] for i in content['pokemon'] ]

    raw_id=generate_random_alphanumeric_string(13)      # Assuming this is ID per ingestion i.e. batch ID
    user_id=generate_random_number(7)
    item_list = []
    for en in effect_entries:
        item = PokemonAbility(
            raw_id=raw_id,
            user_id=user_id,
            pokemon_ability_id=id,
            effect=en['effect'],
            language=en['language'],
            short_effect=en['short_effect']   
        )
        item_list.append(item)
    
    PokemonAbility.bulk_create(item_list)   # Bulk insert is more efficient
    response = {
        'raw_id': raw_id,
        'user_id': user_id,
        'returned_entries': effect_entries,
        'pokemon_list': pokemon_list
    }
    return response


@app.get("/get-ability-from-db/{id}")
async def get_ability(id: int):
    items = PokemonAbility.select().where(PokemonAbility.pokemon_ability_id==id)
    if not items.exists():
        return ResponseObject(success=False, msg=f'Pokemon ability with id {id} doesn\'t exist in db', error='404 data not found')
    return [i for i in items.dicts()]