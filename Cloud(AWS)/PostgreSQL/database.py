from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://your_user:your_password@your-rds-endpoint:5432/your_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
