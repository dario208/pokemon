from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ARRAY, String
from typing import Optional, List

class Pokemon(SQLModel, table=True):
    """Modèle représentant un Pokémon dans la base de données"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # Ajout de unique=True car chaque Pokémon a un nom unique
    types: List[str] = Field(
        sa_column=Column(ARRAY(String)),
        description="Les types du Pokémon (ex: Feu, Eau)"
    )
    total: int = Field(ge=0, description="Somme totale des statistiques")
    hp: int = Field(gt=0, description="Points de vie")
    attack: int = Field(ge=0, description="Attaque physique")
    defense: int = Field(ge=0, description="Défense physique")
    attack_special: int = Field(ge=0, description="Attaque spéciale")
    defense_special: int = Field(ge=0, description="Défense spéciale")
    speed: int = Field(ge=0, description="Vitesse")
    evolution_id: Optional[int] = Field(
        default=None, 
        foreign_key="pokemon.id",
        description="ID du Pokémon évolué (si existant)"
    )