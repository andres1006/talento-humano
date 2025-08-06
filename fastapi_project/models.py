from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# create dictionary to candidate add name cities
def get_name_cities(ciudad_expedicion_rel, ciudad_nacimiento_rel, ciudad_domicilio_rel):
  return {
    "ciudad_expedicion": ciudad_expedicion_rel.nombre if ciudad_expedicion_rel else None,
    "ciudad_nacimiento": ciudad_nacimiento_rel.nombre if ciudad_nacimiento_rel else None,
    "ciudad_domicilio": ciudad_domicilio_rel.nombre if ciudad_domicilio_rel else None
  }
        
class Ciudad(Base):
    __tablename__ = "ciudades"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    departamento = Column(String, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    # Relaciones
    candidatos_nacimiento = relationship("Candidato", foreign_keys="Candidato.ciudad_nacimiento_id", back_populates="ciudad_nacimiento_rel")
    candidatos_expedicion = relationship("Candidato", foreign_keys="Candidato.ciudad_expedicion_id", back_populates="ciudad_expedicion_rel")
    candidatos_domicilio = relationship("Candidato", foreign_keys="Candidato.ciudad_domicilio_id", back_populates="ciudad_domicilio_rel")
    ofertas = relationship("OfertaLaboral", back_populates="ciudad_rel")
    

class Candidato(Base):
    __tablename__ = "candidatos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    tipo_documento = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    rh = Column(String, nullable=False)
    ciudad_expedicion_id = Column(Integer, ForeignKey("ciudades.codigo"), nullable=False)
    ciudad_nacimiento_id = Column(Integer, ForeignKey("ciudades.codigo"), nullable=False)
    ciudad_domicilio_id = Column(Integer, ForeignKey("ciudades.codigo"), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    ciudad_expedicion_rel = relationship("Ciudad", foreign_keys=[ciudad_expedicion_id], back_populates="candidatos_expedicion")
    ciudad_nacimiento_rel = relationship("Ciudad", foreign_keys=[ciudad_nacimiento_id], back_populates="candidatos_nacimiento")
    ciudad_domicilio_rel = relationship("Ciudad", foreign_keys=[ciudad_domicilio_id], back_populates="candidatos_domicilio")
    ofertas_aplicadas = relationship("CandidatoOferta", back_populates="candidato")
    ordenes_asignadas = relationship("CandidatoOrden", back_populates="candidato")


class OfertaLaboral(Base):
    __tablename__ = "ofertas_laborales"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    ciudad_id = Column(Integer, ForeignKey("ciudades.codigo"), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    ciudad_rel = relationship("Ciudad", back_populates="ofertas")
    candidatos_aplicados = relationship("CandidatoOferta", back_populates="oferta")

class OrdenContratacion(Base):
    __tablename__ = "ordenes_contratacion"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    examenes = Column(String, nullable=False)  # Se puede almacenar como JSON string
    
    # Relaciones
    candidatos_asignados = relationship("CandidatoOrden", back_populates="orden")

class CandidatoOferta(Base):
    __tablename__ = "candidato_oferta"
    
    id = Column(Integer, primary_key=True, index=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    oferta_id = Column(Integer, ForeignKey("ofertas_laborales.id"), nullable=False)
    fecha_aplicacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    candidato = relationship("Candidato", back_populates="ofertas_aplicadas")
    oferta = relationship("OfertaLaboral", back_populates="candidatos_aplicados")

class CandidatoOrden(Base):
    __tablename__ = "candidato_orden"
    
    id = Column(Integer, primary_key=True, index=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    orden_id = Column(Integer, ForeignKey("ordenes_contratacion.id"), nullable=False)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    candidato = relationship("Candidato", back_populates="ordenes_asignadas")
    orden = relationship("OrdenContratacion", back_populates="candidatos_asignados")

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    activo = Column(Boolean, default=True, nullable=False) 