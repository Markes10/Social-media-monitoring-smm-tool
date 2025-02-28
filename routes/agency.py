from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Agency

router = APIRouter()

@router.post("/create-agency")
def create_agency(name: str, db: Session = Depends(get_db)):
    if db.query(Agency).filter(Agency.name == name).first():
        return {"message": "Agency already exists"}
    
    agency = Agency(name=name)
    db.add(agency)
    db.commit()
    return {"message": "Agency created successfully"}
