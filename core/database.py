from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Construire l'URL de la base de données manuellement si DATABASE_URL n'est pas défini
POKEMON_USER = os.getenv('POKEMON_USER')
POKEMON_PASSWORD = os.getenv('POKEMON_PASSWORD') 
POKEMON_DB = os.getenv('POKEMON_DB')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    DATABASE_URL = f"postgresql://{POKEMON_USER}:{POKEMON_PASSWORD}@localhost:5432/{POKEMON_DB}"

print("DATABASE_URL:", DATABASE_URL)
print("POKEMON_USER:", POKEMON_USER)
print("POKEMON_PASSWORD:", POKEMON_PASSWORD) 
print("POKEMON_DB:", POKEMON_DB)

# Créer le moteur de base de données avec des paramètres de connexion
engine = create_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10)

def init_db():
    """Initialise la base de données en créant toutes les tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Crée et retourne une session de base de données"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()