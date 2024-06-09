from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config.env import env


engine = create_engine(env["POSTGRES_URI"], echo=False)

db_session = scoped_session(
    sessionmaker(autoflush=False, autocommit=False, bind=engine)
)


def get_db():
    db = None
    try:
        db = db_session()
        yield db
    finally:
        db.close()
