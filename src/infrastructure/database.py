from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión: mysql+driver://usuario:password@host:puerto/nombre_db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/kanban_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()