import json
import logging
from pathlib import Path
from sqlmodel import Session
from models.pokemon_models import Pokemon
from core.database import engine

def clean_pokemon_data(pokemons_data: list) -> list:
    """Nettoie les données en supprimant les références aux évolutions non présentes"""
    available_ids = {pokemon['id'] for pokemon in pokemons_data}
    
    cleaned_data = []
    for pokemon in pokemons_data:
        pokemon_copy = pokemon.copy()
        if 'evolution_id' in pokemon_copy and pokemon_copy['evolution_id'] not in available_ids:
            logging.warning(
                f"Suppression de l'evolution_id {pokemon_copy['evolution_id']} "
                f"pour {pokemon_copy['name']} (évolution non présente dans les données)"
            )
            del pokemon_copy['evolution_id']
        cleaned_data.append(pokemon_copy)
    
    return cleaned_data

def load_data(json_file: str = "pokemons.json") -> None:
    """
    Charge les données des pokémons depuis un fichier JSON dans la base de données.
    
    Args:
        json_file (str): Chemin vers le fichier JSON contenant les données des pokémons
    """
    try:
        file_path = Path(json_file)
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier {json_file} n'existe pas")
            
        with open(file_path, "r", encoding="utf-8") as file:
            pokemons_data = json.load(file)

        # Nettoyer les données avant l'insertion
        cleaned_pokemons = clean_pokemon_data(pokemons_data)

        with Session(engine) as session:
            for pokemon_data in cleaned_pokemons:
                pokemon = Pokemon(**pokemon_data)
                session.add(pokemon)

            session.commit()
            logging.info(f"{len(cleaned_pokemons)} pokémons ont été chargés avec succès")
            
    except Exception as e:
        logging.error(f"Erreur lors du chargement des données: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_data()