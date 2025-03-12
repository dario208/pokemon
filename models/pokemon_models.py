from sqlmodel import SQLModel, Field
from typing import Optional, List

class Pokemon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    types: List[str] = Field(default_factory=list, sa_type="ARRAY(str)")
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Optional[int] = Field(default=None, foreign_key="pokemon.id")