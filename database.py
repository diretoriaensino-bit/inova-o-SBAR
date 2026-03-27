import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, EmailStr
from datetime import datetime

load_dotenv()

# ATENÇÃO: O usuário para a porta 6543 tem que ter o ID do projeto junto!
DB_USER = "postgres.hnkdetbcaozpobutcpxj"
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = "aws-1-us-east-1.pooler.supabase.com"

# URL mágica que resolve o erro "Network Unreachable"
URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:6543/postgres?sslmode=require"

engine = create_engine(URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Tabela onde vamos guardar os SBARs
class SBARSubmission(Base):
    __tablename__ = "sbar_submissions"
    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String)
    situation = Column(Text)
    background = Column(Text)
    assessment = Column(Text)
    recommendation = Column(Text)
    ai_feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

class SBARCreate(BaseModel):
    student_email: EmailStr
    situation: str
    background: str
    assessment: str
    recommendation: str