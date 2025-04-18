# Database setup for SQLModel

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///app/data/scenescope.db"
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from app.models import user, feedback, generation

    SQLModel.metadata.create_all(engine)
