from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import CandidatoOrden
from schemas import CandidatoOrdenCreate

# Operaciones CRUD para CandidatoOrden
def get_candidato_orden(db: Session, candidato_orden_id: int):
    return db.query(CandidatoOrden).filter(CandidatoOrden.id == candidato_orden_id).first()

def get_candidatos_ordenes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CandidatoOrden).offset(skip).limit(limit).all()

def create_candidato_orden(db: Session, candidato_orden: CandidatoOrdenCreate):
    # Verificar que no exista ya la relación
    existing = db.query(CandidatoOrden).filter(
        and_(
            CandidatoOrden.candidato_id == candidato_orden.candidato_id,
            CandidatoOrden.orden_id == candidato_orden.orden_id
        )
    ).first()
    
    if existing:
        return existing
    
    db_candidato_orden = CandidatoOrden(**candidato_orden.dict())
    db.add(db_candidato_orden)
    db.commit()
    db.refresh(db_candidato_orden)
    return db_candidato_orden

def delete_candidato_orden(db: Session, candidato_orden_id: int):
    db_candidato_orden = get_candidato_orden(db, candidato_orden_id)
    if db_candidato_orden:
        db.delete(db_candidato_orden)
        db.commit()
        return True
    return False

# Operaciones adicionales para CandidatoOrden
def get_ordenes_por_candidato(db: Session, candidato_id: int):
    return db.query(CandidatoOrden).filter(CandidatoOrden.candidato_id == candidato_id).all()

def get_candidatos_por_orden(db: Session, orden_id: int):
    return db.query(CandidatoOrden).filter(CandidatoOrden.orden_id == orden_id).all() 