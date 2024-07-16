from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "postgresql://uber:uber@localhost/uberdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UberManagement(Base):
    __tablename__ = 'uber_management'
    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False)
    weekday = Column(String, nullable=False)
    kilometer = Column(Numeric, nullable=False)
    balance_kilometer = Column(Numeric, nullable=False) 
    average_comsuption = Column(Numeric, nullable=False) 
    liter_gasoline_value = Column(Numeric, nullable=False) 
    worked_hours = Column(Numeric, nullable=False) 
    prejudice = Column(Integer, nullable=False)
    receipt_id = Column(ForeignKey("uber_management_receipts.id"), nullable=False) 
    receipt = relationship("UberManagementReceipts", back_populates="uber_managements")
    
class UberManagementReceipts(Base):
    __tablename__ = 'uber_management_receipts'
    id = Column(Integer, primary_key=True)
    uber_value = Column(Numeric, nullable=False)
    pop_99_value = Column(Numeric, nullable=False)
    promotions = Column(Numeric, nullable=False)
    run_outside = Column(Numeric, nullable=False)
    uber_managements = relationship("UberManagement", back_populates="receipt")

    

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()