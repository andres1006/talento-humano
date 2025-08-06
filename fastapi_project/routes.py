from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import (
    # Ciudad CRUD
    get_ciudad, get_ciudades, create_ciudad as crud_create_ciudad, update_ciudad as crud_update_ciudad, delete_ciudad as crud_delete_ciudad,
    # Candidato CRUD
    get_candidato, get_candidatos, create_candidato as crud_create_candidato, update_candidato as crud_update_candidato, delete_candidato as crud_delete_candidato, get_candidatos_por_ciudad,
    get_candidato_con_nombres_ciudades, get_candidatos_con_nombres_ciudades,
    # Oferta Laboral CRUD
    get_oferta, get_ofertas, create_oferta as crud_create_oferta, update_oferta as crud_update_oferta, delete_oferta as crud_delete_oferta, get_ofertas_por_ciudad,
    get_oferta_con_nombre_ciudad, get_ofertas_con_nombre_ciudad,
    # Orden Contratacion CRUD
    get_orden, get_ordenes, create_orden as crud_create_orden, update_orden as crud_update_orden, delete_orden as crud_delete_orden,
    # CandidatoOferta CRUD
    get_candidato_oferta, get_candidatos_ofertas, create_candidato_oferta as crud_create_candidato_oferta, delete_candidato_oferta as crud_delete_candidato_oferta,
    get_candidatos_por_oferta, get_ofertas_por_candidato,
    # CandidatoOrden CRUD
    get_candidato_orden, get_candidatos_ordenes, create_candidato_orden as crud_create_candidato_orden, delete_candidato_orden as crud_delete_candidato_orden,
    get_ordenes_por_candidato, get_candidatos_por_orden,
    # Cliente CRUD
    get_cliente, get_clientes, create_cliente as crud_create_cliente, update_cliente as crud_update_cliente, delete_cliente as crud_delete_cliente, toggle_cliente_status
)
from models import Candidato, OfertaLaboral, OrdenContratacion, CandidatoOferta, CandidatoOrden, Ciudad, Cliente, get_name_cities
import schemas

router = APIRouter()

# Rutas para Ciudades
@router.post("/ciudades/", response_model=schemas.Ciudad)
def create_ciudad(ciudad: schemas.CiudadCreate, db: Session = Depends(get_db)):
    return crud_create_ciudad(db=db, ciudad=ciudad)

@router.get("/ciudades/", response_model=List[schemas.Ciudad])
def read_ciudades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ciudades = get_ciudades(db, skip=skip, limit=limit)
    return ciudades

@router.get("/ciudades/{ciudad_id}", response_model=schemas.Ciudad)
def read_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    db_ciudad = get_ciudad(db, ciudad_id=ciudad_id)
    if db_ciudad is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return db_ciudad

@router.put("/ciudades/{ciudad_id}", response_model=schemas.Ciudad)
def update_ciudad(ciudad_id: int, ciudad: schemas.CiudadCreate, db: Session = Depends(get_db)):
    db_ciudad = crud_update_ciudad(db, ciudad_id, ciudad.dict())
    if db_ciudad is None:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return db_ciudad

@router.delete("/ciudades/{ciudad_id}")
def delete_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    success = crud_delete_ciudad(db, ciudad_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return {"message": "Ciudad eliminada exitosamente"}

# Rutas para Candidatos
@router.post("/candidatos/", response_model=schemas.CandidatoConNombresCiudades)
def create_candidato(candidato: schemas.CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = crud_create_candidato(db=db, candidato=candidato)
    # Obtener el candidato con nombres de ciudades
    return get_candidato_con_nombres_ciudades(db, db_candidato.id)

@router.get("/candidatos/", response_model=List[schemas.CandidatoConNombresCiudades])
def read_candidatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    candidatos = get_candidatos_con_nombres_ciudades(db, skip=skip, limit=limit)
    return candidatos

@router.get("/candidatos/{candidato_id}", response_model=schemas.CandidatoConNombresCiudades)
def read_candidato(candidato_id: int, db: Session = Depends(get_db)):
    db_candidato = get_candidato_con_nombres_ciudades(db, candidato_id=candidato_id)
    if db_candidato is None:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return db_candidato

@router.put("/candidatos/{candidato_id}", response_model=schemas.CandidatoConNombresCiudades)
def update_candidato(candidato_id: int, candidato: schemas.CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = crud_update_candidato(db, candidato_id, candidato.dict())
    if db_candidato is None:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    # Obtener el candidato actualizado con nombres de ciudades
    return get_candidato_con_nombres_ciudades(db, candidato_id)

@router.delete("/candidatos/{candidato_id}")
def delete_candidato(candidato_id: int, db: Session = Depends(get_db)):
    success = crud_delete_candidato(db, candidato_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return {"message": "Candidato eliminado exitosamente"}

# Rutas para Ofertas Laborales
@router.post("/ofertas/", response_model=schemas.OfertaLaboralConNombreCiudad)
def create_oferta(oferta: schemas.OfertaLaboralCreate, db: Session = Depends(get_db)):
    db_oferta = crud_create_oferta(db=db, oferta=oferta)
    # Obtener la oferta con nombre de ciudad
    return get_oferta_con_nombre_ciudad(db, db_oferta.id)

@router.get("/ofertas/", response_model=List[schemas.OfertaLaboralConNombreCiudad])
def read_ofertas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ofertas = get_ofertas_con_nombre_ciudad(db, skip=skip, limit=limit)
    return ofertas

@router.get("/ofertas/{oferta_id}", response_model=schemas.OfertaLaboralConNombreCiudad)
def read_oferta(oferta_id: int, db: Session = Depends(get_db)):
    db_oferta = get_oferta_con_nombre_ciudad(db, oferta_id=oferta_id)
    if db_oferta is None:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return db_oferta

@router.put("/ofertas/{oferta_id}", response_model=schemas.OfertaLaboralConNombreCiudad)
def update_oferta(oferta_id: int, oferta: schemas.OfertaLaboralCreate, db: Session = Depends(get_db)):
    db_oferta = crud_update_oferta(db, oferta_id, oferta.dict())
    if db_oferta is None:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    # Obtener la oferta actualizada con nombre de ciudad
    return get_oferta_con_nombre_ciudad(db, oferta_id)

@router.delete("/ofertas/{oferta_id}")
def delete_oferta(oferta_id: int, db: Session = Depends(get_db)):
    success = crud_delete_oferta(db, oferta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return {"message": "Oferta eliminada exitosamente"}

# Rutas para Órdenes de Contratación
@router.post("/ordenes/", response_model=schemas.OrdenContratacion)
def create_orden(orden: schemas.OrdenContratacionCreate, db: Session = Depends(get_db)):
    return crud_create_orden(db=db, orden=orden)

@router.get("/ordenes/", response_model=List[schemas.OrdenContratacion])
def read_ordenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ordenes = get_ordenes(db, skip=skip, limit=limit)
    return ordenes

@router.get("/ordenes/{orden_id}", response_model=schemas.OrdenContratacion)
def read_orden(orden_id: int, db: Session = Depends(get_db)):
    db_orden = get_orden(db, orden_id=orden_id)
    if db_orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_orden

@router.put("/ordenes/{orden_id}", response_model=schemas.OrdenContratacion)
def update_orden(orden_id: int, orden: schemas.OrdenContratacionCreate, db: Session = Depends(get_db)):
    db_orden = crud_update_orden(db, orden_id, orden.dict())
    if db_orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_orden

@router.delete("/ordenes/{orden_id}")
def delete_orden(orden_id: int, db: Session = Depends(get_db)):
    success = crud_delete_orden(db, orden_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada exitosamente"}

# Rutas para CandidatoOferta (Aplicaciones)
@router.post("/candidatos/{candidato_id}/aplicar/{oferta_id}", response_model=schemas.CandidatoOferta)
def aplicar_a_oferta(candidato_id: int, oferta_id: int, db: Session = Depends(get_db)):
    candidato_oferta = schemas.CandidatoOfertaCreate(candidato_id=candidato_id, oferta_id=oferta_id)
    return crud_create_candidato_oferta(db=db, candidato_oferta=candidato_oferta)

@router.get("/candidatos/{candidato_id}/ofertas", response_model=List[schemas.CandidatoOferta])
def get_ofertas_candidato(candidato_id: int, db: Session = Depends(get_db)):
    return get_ofertas_por_candidato(db, candidato_id)

@router.get("/ofertas/{oferta_id}/candidatos", response_model=List[schemas.CandidatoOferta])
def get_candidatos_oferta(oferta_id: int, db: Session = Depends(get_db)):
    return get_candidatos_por_oferta(db, oferta_id)

@router.delete("/candidatos/{candidato_id}/ofertas/{oferta_id}")
def cancelar_aplicacion(candidato_id: int, oferta_id: int, db: Session = Depends(get_db)):
    # Buscar la relación específica
    candidato_oferta = db.query(CandidatoOferta).filter(
        CandidatoOferta.candidato_id == candidato_id,
        CandidatoOferta.oferta_id == oferta_id
    ).first()
    
    if not candidato_oferta:
        raise HTTPException(status_code=404, detail="Aplicación no encontrada")
    
    db.delete(candidato_oferta)
    db.commit()
    return {"message": "Aplicación cancelada exitosamente"}

# Rutas para CandidatoOrden (Asignaciones)
@router.post("/candidatos/{candidato_id}/asignar/{orden_id}", response_model=schemas.CandidatoOrden)
def asignar_a_orden(candidato_id: int, orden_id: int, db: Session = Depends(get_db)):
    candidato_orden = schemas.CandidatoOrdenCreate(candidato_id=candidato_id, orden_id=orden_id)
    return crud_create_candidato_orden(db=db, candidato_orden=candidato_orden)

@router.get("/candidatos/{candidato_id}/ordenes", response_model=List[schemas.CandidatoOrden])
def get_ordenes_candidato(candidato_id: int, db: Session = Depends(get_db)):
    return get_ordenes_por_candidato(db, candidato_id)

@router.get("/ordenes/{orden_id}/candidatos", response_model=List[schemas.CandidatoOrden])
def get_candidatos_orden(orden_id: int, db: Session = Depends(get_db)):
    return get_candidatos_por_orden(db, orden_id)

@router.delete("/candidatos/{candidato_id}/ordenes/{orden_id}")
def cancelar_asignacion(candidato_id: int, orden_id: int, db: Session = Depends(get_db)):
    # Buscar la relación específica
    candidato_orden = db.query(CandidatoOrden).filter(
        CandidatoOrden.candidato_id == candidato_id,
        CandidatoOrden.orden_id == orden_id
    ).first()
    
    if not candidato_orden:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    db.delete(candidato_orden)
    db.commit()
    return {"message": "Asignación cancelada exitosamente"}

# Rutas adicionales para ciudades
@router.get("/ciudades/{ciudad_id}/candidatos", response_model=List[schemas.CandidatoConNombresCiudades])
def get_candidatos_por_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    candidatos = get_candidatos_por_ciudad(db, ciudad_id)
    # Agregar nombres de ciudades a cada candidato
    for candidato in candidatos:
        nombres_ciudades = get_name_cities(
            candidato.ciudad_expedicion_rel,
            candidato.ciudad_nacimiento_rel,
            candidato.ciudad_domicilio_rel
        )
        candidato.nombres_ciudades = nombres_ciudades
    return candidatos

@router.get("/ciudades/{ciudad_id}/ofertas", response_model=List[schemas.OfertaLaboralConNombreCiudad])
def get_ofertas_por_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    ofertas = get_ofertas_por_ciudad(db, ciudad_id)
    # Agregar nombre de ciudad a cada oferta
    for oferta in ofertas:
        if oferta.ciudad_rel:
            oferta.nombre_ciudad = oferta.ciudad_rel.nombre
    return ofertas

# Rutas adicionales útiles
@router.get("/estadisticas/")
def get_estadisticas(db: Session = Depends(get_db)):
    total_candidatos = db.query(Candidato).count()
    total_ofertas = db.query(OfertaLaboral).count()
    total_ordenes = db.query(OrdenContratacion).count()
    total_aplicaciones = db.query(CandidatoOferta).count()
    total_asignaciones = db.query(CandidatoOrden).count()
    total_ciudades = db.query(Ciudad).count()
    
    return {
        "total_candidatos": total_candidatos,
        "total_ofertas": total_ofertas,
        "total_ordenes": total_ordenes,
        "total_aplicaciones": total_aplicaciones,
        "total_asignaciones": total_asignaciones,
        "total_ciudades": total_ciudades
    }

# Rutas para Clientes
@router.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud_create_cliente(db=db, cliente=cliente)

@router.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud_update_cliente(db, cliente_id, cliente.dict())
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    success = crud_delete_cliente(db, cliente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}

@router.patch("/clientes/{cliente_id}/toggle-status", response_model=schemas.Cliente)
def toggle_cliente_status_route(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = toggle_cliente_status(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente 