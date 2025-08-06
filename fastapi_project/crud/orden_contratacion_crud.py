from sqlalchemy.orm import Session
from models import OrdenContratacion
from schemas import OrdenContratacionCreate

# Operaciones CRUD para Órdenes de Contratación
def get_orden(db: Session, orden_id: int):
    return db.query(OrdenContratacion).filter(OrdenContratacion.id == orden_id).first()

def get_ordenes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrdenContratacion).offset(skip).limit(limit).all()

def create_orden(db: Session, orden: OrdenContratacionCreate):
    db_orden = OrdenContratacion(**orden.dict())
    db.add(db_orden)
    db.commit()
    db.refresh(db_orden)
    return db_orden

def update_orden(db: Session, orden_id: int, orden_data: dict):
    db_orden = get_orden(db, orden_id)
    if db_orden:
        for key, value in orden_data.items():
            setattr(db_orden, key, value)
        db.commit()
        db.refresh(db_orden)
    return db_orden

def delete_orden(db: Session, orden_id: int):
    db_orden = get_orden(db, orden_id)
    if db_orden:
        db.delete(db_orden)
        db.commit()
        return True
    return False 