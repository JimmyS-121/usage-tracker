from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, analysis

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usage/", response_model=schemas.UsageRecord)
def create_usage_record(record: schemas.UsageRecordCreate, db: Session = Depends(get_db)):
    db_record = models.UsageRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/analysis/")
def get_analysis(db: Session = Depends(get_db)):
    return analysis.get_latest_analysis(db)
