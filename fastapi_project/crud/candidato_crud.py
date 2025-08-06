from sqlalchemy.orm import Session
from models import Candidato, get_name_cities
from schemas import CandidatoCreate

# Operaciones CRUD para Candidatos
def get_candidato(db: Session, candidato_id: int):
    return db.query(Candidato).filter(Candidato.id == candidato_id).first()

def get_candidatos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Candidato).offset(skip).limit(limit).all()

def create_candidato(db: Session, candidato: CandidatoCreate):
    db_candidato = Candidato(**candidato.dict())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

def update_candidato(db: Session, candidato_id: int, candidato_data: dict):
    db_candidato = get_candidato(db, candidato_id)
    if db_candidato:
        for key, value in candidato_data.items():
            setattr(db_candidato, key, value)
        db.commit()
        db.refresh(db_candidato)
    return db_candidato

def delete_candidato(db: Session, candidato_id: int):
    db_candidato = get_candidato(db, candidato_id)
    if db_candidato:
        db.delete(db_candidato)
        db.commit()
        return True
    return False

# Operaciones adicionales para Candidatos
def get_candidatos_por_ciudad(db: Session, ciudad_id: int):
    return db.query(Candidato).filter(
        (Candidato.ciudad_nacimiento_id == ciudad_id) |
        (Candidato.ciudad_expedicion_id == ciudad_id) |
        (Candidato.ciudad_domicilio_id == ciudad_id)
    ).all()

# Nuevas funciones para obtener candidatos con nombres de ciudades
def get_candidato_con_nombres_ciudades(db: Session, candidato_id: int):
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if candidato:
        nombres_ciudades = get_name_cities(
            candidato.ciudad_expedicion_rel,
            candidato.ciudad_nacimiento_rel,
            candidato.ciudad_domicilio_rel
        )
        # Agregar los nombres de ciudades como atributo del candidato
        candidato.nombres_ciudades = nombres_ciudades
    return candidato

def get_candidatos_con_nombres_ciudades(db: Session, skip: int = 0, limit: int = 100):
    candidatos = db.query(Candidato).offset(skip).limit(limit).all()
    for candidato in candidatos:
        nombres_ciudades = get_name_cities(
            candidato.ciudad_expedicion_rel,
            candidato.ciudad_nacimiento_rel,
            candidato.ciudad_domicilio_rel
        )
        candidato.nombres_ciudades = nombres_ciudades
    return candidatos 