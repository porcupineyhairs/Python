from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(r"mssql+pymssql://sa:COMfort123456@192.168.0.198/TEST_DB?charset=GBK")

DBsession = sessionmaker(bind=engine, autoflush=True, autocommit=False)


class Users(Base):
    __tablename__ = 'WG_USER'
    T1 = Column('U_ID', primary_key=True)
    T2 = Column('FLAG')
    T3 = Column('U_NAME')
    

class ZYH005(Base):
    __tablename__ = 'ZYH005'
    T1 = Column('ZN001', primary_key=True)
    T2 = Column('ZN002')
    T3 = Column('ZN003')
    

class MDDZ(Base):
    __tablename__ = 'MDDZ'
    T1 = Column('MD_NO', primary_key=True)
    T2 = Column('SC001')


session = DBsession()

dt = Users(T1='445', T2='N'.encode('GBK'), T3='你好'.encode('GBK'))
session.add(dt)
session.commit()

