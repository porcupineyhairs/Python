from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mssql+pymssql://sa:COMfort123456@192.168.0.198:1433/COMFORT")

Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)

print(Session)
