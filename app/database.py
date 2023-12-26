from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@postgresserver-ip-address/dbName"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pgAdminPasswordDB@localhost/fastapitutorial"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
