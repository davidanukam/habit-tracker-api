from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# To START running postgreSQL 18 server: net start postgresql-x64-18
# To STOP running postgreSQL 18 server: net stop postgresql-x64-18

DATABASE_URL = (
    "postgresql+psycopg2://postgres:root@localhost:5432/habit_tracker_api_database"
)

engine = create_engine(DATABASE_URL)

# autoflush means changes stay in Python memory until I explicitly flush or commit them
# autocommit means changes stay in a pending transaction until I call session.commit()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# Dependency to inject database sessions into API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # Automatically rolls back if an endpoint raises an error
        db.rollback()
        raise
    finally:
        db.close()
