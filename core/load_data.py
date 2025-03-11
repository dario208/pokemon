import json
from sqlmodel import Session
from models import Pokemon
from database import engine

def load_data():
    with open("pokemons.json", "r") as file:
        pokemons_data = json.load(file)

    with Session(engine) as session:
        for pokemon_data in pokemons_data:
            pokemon = Pokemon(**pokemon_data)
            session.add(pokemon)
        session.commit()

if __name__ == "__main__":
    load_data()