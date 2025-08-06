from sqlalchemy.orm import Session
from models import OfertaLaboral
from schemas import OfertaLaboralCreate

# Operaciones CRUD para Ofertas Laborales
def get_oferta(db: Session, oferta_id: int):
    return db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()

def get_ofertas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OfertaLaboral).offset(skip).limit(limit).all()

def create_oferta(db: Session, oferta: OfertaLaboralCreate):
    db_oferta = OfertaLaboral(**oferta.dict())
    db.add(db_oferta)
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

def update_oferta(db: Session, oferta_id: int, oferta_data: dict):
    db_oferta = get_oferta(db, oferta_id)
    if db_oferta:
        for key, value in oferta_data.items():
            setattr(db_oferta, key, value)
        db.commit()
        db.refresh(db_oferta)
    return db_oferta

def delete_oferta(db: Session, oferta_id: int):
    db_oferta = get_oferta(db, oferta_id)
    if db_oferta:
        db.delete(db_oferta)
        db.commit()
        return True
    return False

# Operaciones adicionales para Ofertas Laborales
def get_ofertas_por_ciudad(db: Session, ciudad_id: int):
    return db.query(OfertaLaboral).filter(OfertaLaboral.ciudad_id == ciudad_id).all()

# Nuevas funciones para obtener ofertas con nombre de ciudad
def get_oferta_con_nombre_ciudad(db: Session, oferta_id: int):
    oferta = db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()
    if oferta and oferta.ciudad_rel:
        oferta.nombre_ciudad = oferta.ciudad_rel.nombre
    return oferta

def get_ofertas_con_nombre_ciudad(db: Session, skip: int = 0, limit: int = 100):
    ofertas = db.query(OfertaLaboral).offset(skip).limit(limit).all()
    for oferta in ofertas:
        if oferta.ciudad_rel:
            oferta.nombre_ciudad = oferta.ciudad_rel.nombre
    return ofertas 