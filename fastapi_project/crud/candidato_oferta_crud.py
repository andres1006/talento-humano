from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import CandidatoOferta
from schemas import CandidatoOfertaCreate

# Operaciones CRUD para CandidatoOferta
def get_candidato_oferta(db: Session, candidato_oferta_id: int):
    return db.query(CandidatoOferta).filter(CandidatoOferta.id == candidato_oferta_id).first()

def get_candidatos_ofertas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CandidatoOferta).offset(skip).limit(limit).all()

def create_candidato_oferta(db: Session, candidato_oferta: CandidatoOfertaCreate):
    # Verificar que no exista ya la relación
    existing = db.query(CandidatoOferta).filter(
        and_(
            CandidatoOferta.candidato_id == candidato_oferta.candidato_id,
            CandidatoOferta.oferta_id == candidato_oferta.oferta_id
        )
    ).first()
    
    if existing:
        return existing
    
    db_candidato_oferta = CandidatoOferta(**candidato_oferta.dict())
    db.add(db_candidato_oferta)
    db.commit()
    db.refresh(db_candidato_oferta)
    return db_candidato_oferta

def delete_candidato_oferta(db: Session, candidato_oferta_id: int):
    db_candidato_oferta = get_candidato_oferta(db, candidato_oferta_id)
    if db_candidato_oferta:
        db.delete(db_candidato_oferta)
        db.commit()
        return True
    return False

# Operaciones adicionales para CandidatoOferta
def get_candidatos_por_oferta(db: Session, oferta_id: int):
    return db.query(CandidatoOferta).filter(CandidatoOferta.oferta_id == oferta_id).all()

def get_ofertas_por_candidato(db: Session, candidato_id: int):
    return db.query(CandidatoOferta).filter(CandidatoOferta.candidato_id == candidato_id).all() 