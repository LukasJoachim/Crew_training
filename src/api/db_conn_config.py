import os

DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),  
    "port": os.getenv("POSTGRES_PORT", 5432),
    "database": os.getenv("POSTGRES_DB", "crew_training"),
    "user": os.getenv("POSTGRES_USER", "admin"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
}


