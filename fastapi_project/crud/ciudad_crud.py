from sqlalchemy.orm import Session
from models import Ciudad
from schemas import CiudadCreate

# Operaciones CRUD para Ciudades
def get_ciudad(db: Session, ciudad_id: int):
    return db.query(Ciudad).filter(Ciudad.id == ciudad_id).first()

def get_ciudad_by_codigo(db: Session, codigo: str):
    return db.query(Ciudad).filter(Ciudad.codigo == codigo).first()

def get_ciudades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ciudad).offset(skip).limit(limit).all()

def create_ciudad(db: Session, ciudad: CiudadCreate):
    db_ciudad = Ciudad(**ciudad.dict())
    db.add(db_ciudad)
    db.commit()
    db.refresh(db_ciudad)
    return db_ciudad

def update_ciudad(db: Session, ciudad_id: int, ciudad_data: dict):
    db_ciudad = get_ciudad(db, ciudad_id)
    if db_ciudad:
        for key, value in ciudad_data.items():
            setattr(db_ciudad, key, value)
        db.commit()
        db.refresh(db_ciudad)
    return db_ciudad

def delete_ciudad(db: Session, ciudad_id: int):
    db_ciudad = get_ciudad(db, ciudad_id)
    if db_ciudad:
        db.delete(db_ciudad)
        db.commit()
        return True
    return False 