from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models.pokemon_models import Pokemon
from core.database import init_db, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/pokemons/", response_model=list[Pokemon])
def read_pokemons(session: Session = Depends(get_session)):
    pokemons = session.exec(select(Pokemon)).all()
    return pokemons

@app.get("/pokemons/{pokemon_id}", response_model=Pokemon)
def read_pokemon(pokemon_id: int, session: Session = Depends(get_session)):
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon

@app.post("/pokemons/", response_model=Pokemon)
def create_pokemon(pokemon: Pokemon, session: Session = Depends(get_session)):
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon

@app.put("/pokemons/{pokemon_id}", response_model=Pokemon)
def update_pokemon(pokemon_id: int, pokemon: Pokemon, session: Session = Depends(get_session)):
    db_pokemon = session.get(Pokemon, pokemon_id)
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    for key, value in pokemon.dict().items():
        setattr(db_pokemon, key, value)
    session.add(db_pokemon)
    session.commit()
    session.refresh(db_pokemon)
    return db_pokemon

@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int, session: Session = Depends(get_session)):
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    session.delete(pokemon)
    session.commit()
    return {"ok": True}