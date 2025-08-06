from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict

# Esquemas para Ciudades
class CiudadBase(BaseModel):
    codigo: str
    nombre: str
    departamento: Optional[str] = None

class CiudadCreate(CiudadBase):
    pass

class Ciudad(CiudadBase):
    id: int
    
    class Config:
        from_attributes = True

# Esquemas para Candidatos
class CandidatoBase(BaseModel):
    nombre: str
    apellido: str
    tipo_documento: str
    cedula: str
    fecha_nacimiento: date
    rh: str
    ciudad_expedicion_id: int
    ciudad_nacimiento_id: int
    ciudad_domicilio_id: int
    activo: bool = True

class CandidatoCreate(CandidatoBase):
    pass

class Candidato(CandidatoBase):
    id: int
    
    class Config:
        from_attributes = True

# Nuevo esquema para candidatos con nombres de ciudades como diccionario
class CandidatoConNombresCiudades(Candidato):
    nombres_ciudades: Dict[str, Optional[str]] = {
        "ciudad_expedicion": None,
        "ciudad_nacimiento": None,
        "ciudad_domicilio": None
    }
    
    class Config:
        from_attributes = True

# Esquemas para Ofertas Laborales
class OfertaLaboralBase(BaseModel):
    cliente: str
    cargo: str
    descripcion: str
    ciudad_id: int
    activo: bool = True

class OfertaLaboralCreate(OfertaLaboralBase):
    pass

class OfertaLaboral(OfertaLaboralBase):
    id: int
    
    class Config:
        from_attributes = True

# Nuevo esquema para ofertas con nombre de ciudad como diccionario
class OfertaLaboralConNombreCiudad(OfertaLaboral):
    nombre_ciudad: Optional[str] = None
    
    class Config:
        from_attributes = True

# Esquemas para Órdenes de Contratación
class OrdenContratacionBase(BaseModel):
    cliente: str
    cargo: str
    examenes: str

class OrdenContratacionCreate(OrdenContratacionBase):
    pass

class OrdenContratacion(OrdenContratacionBase):
    id: int
    
    class Config:
        from_attributes = True

# Esquemas para CandidatoOferta
class CandidatoOfertaBase(BaseModel):
    candidato_id: int
    oferta_id: int

class CandidatoOfertaCreate(CandidatoOfertaBase):
    pass

class CandidatoOferta(CandidatoOfertaBase):
    id: int
    fecha_aplicacion: datetime
    
    class Config:
        from_attributes = True

# Esquemas para CandidatoOrden
class CandidatoOrdenBase(BaseModel):
    candidato_id: int
    orden_id: int

class CandidatoOrdenCreate(CandidatoOrdenBase):
    pass

class CandidatoOrden(CandidatoOrdenBase):
    id: int
    fecha_asignacion: datetime
    
    class Config:
        from_attributes = True

# Esquemas con relaciones
class CandidatoConOfertas(Candidato):
    ofertas_aplicadas: List[CandidatoOferta] = []

class CandidatoConOrdenes(Candidato):
    ordenes_asignadas: List[CandidatoOrden] = []

class OfertaLaboralConCandidatos(OfertaLaboral):
    candidatos_aplicados: List[CandidatoOferta] = []

class OrdenContratacionConCandidatos(OrdenContratacion):
    candidatos_asignados: List[CandidatoOrden] = []

# Esquemas con información de ciudades
class CandidatoConCiudades(Candidato):
    ciudad_expedicion: Optional[Ciudad] = None
    ciudad_nacimiento: Optional[Ciudad] = None
    ciudad_domicilio: Optional[Ciudad] = None

class OfertaLaboralConCiudad(OfertaLaboral):
    ciudad: Optional[Ciudad] = None

# Esquemas para Clientes
class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    activo: bool = True

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    
    class Config:
        from_attributes = True 