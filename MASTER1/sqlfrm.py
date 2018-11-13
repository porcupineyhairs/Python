from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine("mssql+pymssql://sa:COMfort123456@192.168.0.198:1433/WG_DB")

session = sessionmaker(bind=engine, autoflush=True, autocommit=False)

print(session)

class Users(Base):
    __tablename__ = 'WG_APP_INF'



ret = session.query(Users).all()
ret = session.query(Users).filter_by(Version='2.1.5').first()

print(type(ret))
print(ret)
