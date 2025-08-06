from database import SessionLocal, engine
from models import Base, Candidato, OfertaLaboral, OrdenContratacion, Ciudad
from datetime import date
import json
import os

Base.metadata.create_all(bind=engine)

def mapear_ciudad(codigo_ciudad):
    """Mapea códigos de ciudad a nombres de ciudades"""
    mapeo_ciudades = {
        "1011": "Bogotá",
        "3001": "Medellín", 
        "402": "Cali",
        "5001": "Barranquilla",
        "11001": "Bucaramanga",
        "13001": "Cartagena",
        "15001": "Tunja",
        "17001": "Manizales",
        "19001": "Pasto",
        "20001": "Valledupar",
        "23001": "Montería",
        "25001": "Villavicencio",
        "27001": "Quibdó",
        "41001": "Neiva",
        "44001": "Riohacha",
        "47001": "Santa Marta",
        "50001": "Armenia",
        "52001": "Pereira",
        "54001": "Cúcuta",
        "63001": "Popayán",
        "66001": "Pereira",
        "68001": "Bucaramanga",
        "70001": "Sincelejo",
        "73001": "Ibagué",
        "76001": "Cali",
        "81001": "Arauca",
        "85001": "Yopal",
        "88001": "San Andrés",
        "91001": "Leticia",
        "94001": "Inírida",
        "95001": "San José del Guaviare",
        "97001": "Mitú",
        "99001": "Puerto Carreño"
    }
    return mapeo_ciudades.get(codigo_ciudad, f"Ciudad {codigo_ciudad}")

def generar_fecha_nacimiento():
    """Genera una fecha de nacimiento aleatoria para los candidatos"""
    import random
    from datetime import datetime, timedelta
    
    # Generar fecha entre 1980 y 2005
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2005, 12, 31)
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    
    return random_date.date()

def init_db():
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Candidato).count() > 0:
            print("La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        # Crear ciudades primero
        print("Creando ciudades...")
        ciudades_data = {
            "1011": {"nombre": "Bogotá", "departamento": "Cundinamarca"},
            "3001": {"nombre": "Medellín", "departamento": "Antioquia"},
            "402": {"nombre": "Cali", "departamento": "Valle del Cauca"},
            "5001": {"nombre": "Barranquilla", "departamento": "Atlántico"},
            "11001": {"nombre": "Bucaramanga", "departamento": "Santander"},
            "13001": {"nombre": "Cartagena", "departamento": "Bolívar"},
            "15001": {"nombre": "Tunja", "departamento": "Boyacá"},
            "17001": {"nombre": "Manizales", "departamento": "Caldas"},
            "19001": {"nombre": "Pasto", "departamento": "Nariño"},
            "20001": {"nombre": "Valledupar", "departamento": "Cesar"},
            "23001": {"nombre": "Montería", "departamento": "Córdoba"},
            "25001": {"nombre": "Villavicencio", "departamento": "Meta"},
            "27001": {"nombre": "Quibdó", "departamento": "Chocó"},
            "41001": {"nombre": "Neiva", "departamento": "Huila"},
            "44001": {"nombre": "Riohacha", "departamento": "La Guajira"},
            "47001": {"nombre": "Santa Marta", "departamento": "Magdalena"},
            "50001": {"nombre": "Armenia", "departamento": "Quindío"},
            "52001": {"nombre": "Pereira", "departamento": "Risaralda"},
            "54001": {"nombre": "Cúcuta", "departamento": "Norte de Santander"},
            "63001": {"nombre": "Popayán", "departamento": "Cauca"},
            "70001": {"nombre": "Sincelejo", "departamento": "Sucre"},
            "73001": {"nombre": "Ibagué", "departamento": "Tolima"},
            "81001": {"nombre": "Arauca", "departamento": "Arauca"},
            "85001": {"nombre": "Yopal", "departamento": "Casanare"},
            "88001": {"nombre": "San Andrés", "departamento": "San Andrés y Providencia"},
            "91001": {"nombre": "Leticia", "departamento": "Amazonas"},
            "94001": {"nombre": "Inírida", "departamento": "Guainía"},
            "95001": {"nombre": "San José del Guaviare", "departamento": "Guaviare"},
            "97001": {"nombre": "Mitú", "departamento": "Vaupés"},
            "99001": {"nombre": "Puerto Carreño", "departamento": "Vichada"}
        }
        
        ciudades_creadas = {}
        for codigo, info in ciudades_data.items():
            ciudad = Ciudad(
                codigo=codigo,
                nombre=info["nombre"],
                departamento=info["departamento"]
            )
            db.add(ciudad)
            ciudades_creadas[codigo] = ciudad
        
        db.commit()
        print(f"✅ {len(ciudades_creadas)} ciudades creadas")
        
        # Cargar datos del JSON
        json_path = os.path.join(os.path.dirname(__file__), '..', 'JSON.txt')
        with open(json_path, 'r', encoding='utf-8') as file:
            candidatos_data = json.load(file)
        
        print(f"Cargando {len(candidatos_data)} candidatos desde el JSON...")
        
        # Crear candidatos desde el JSON
        candidatos = []
        for i, candidato_data in enumerate(candidatos_data):
            # Generar fecha de nacimiento aleatoria
            fecha_nacimiento = generar_fecha_nacimiento()
            
            # Obtener IDs de ciudades
            ciudad_expedicion_id = ciudades_creadas.get(candidato_data["ciudad_e"], ciudades_creadas["1011"]).codigo    
            ciudad_nacimiento_id = ciudades_creadas.get(candidato_data["ciudad_n"], ciudades_creadas["1011"]).codigo
            ciudad_domicilio_id = ciudades_creadas.get(candidato_data["ciudad_d"], ciudades_creadas["1011"]).codigo
            
            candidato = Candidato(
                nombre=candidato_data["nombre"],
                apellido=candidato_data["apellido"],
                tipo_documento=candidato_data["clasE_DOCTO"],
                cedula=candidato_data["doctO_IDENT"],
                fecha_nacimiento=fecha_nacimiento,
                rh=candidato_data["grupO_RH"],
                ciudad_expedicion_id=ciudad_expedicion_id,
                ciudad_nacimiento_id=ciudad_nacimiento_id,
                ciudad_domicilio_id=ciudad_domicilio_id
            )
            candidatos.append(candidato)
            
            # Mostrar progreso cada 50 candidatos
            if (i + 1) % 50 == 0:
                print(f"Procesados {i + 1} candidatos...")
        
        # Agregar candidatos a la base de datos
        for candidato in candidatos:
            db.add(candidato)
        
        # Crear ofertas laborales de ejemplo
        ofertas = [
            OfertaLaboral(
                cliente="Empresa ABC",
                cargo="Desarrollador Full Stack",
                descripcion="Buscamos desarrollador con experiencia en React y Python",
                ciudad_id=ciudades_creadas["1011"].codigo  # Bogotá
            ),
            OfertaLaboral(
                cliente="Empresa XYZ",
                cargo="Analista de Datos",
                descripcion="Analista con experiencia en SQL y Python",
                ciudad_id=ciudades_creadas["3001"].codigo  # Medellín
            ),
            OfertaLaboral(
                cliente="Startup Tech",
                cargo="DevOps Engineer",
                descripcion="Ingeniero DevOps con experiencia en AWS y Docker",
                ciudad_id=ciudades_creadas["402"].codigo  # Cali
            ),
            OfertaLaboral(
                cliente="Corporación Digital",
                cargo="Desarrollador Frontend",
                descripcion="Desarrollador con experiencia en React, Vue.js y TypeScript",
                ciudad_id=ciudades_creadas["1011"].codigo  # Bogotá
            ),
            OfertaLaboral(
                cliente="Tech Solutions",
                cargo="Desarrollador Backend",
                descripcion="Desarrollador con experiencia en Java, Spring Boot y microservicios",
                ciudad_id=ciudades_creadas["3001"].codigo  # Medellín
            )
        ]
        
        for oferta in ofertas:
            db.add(oferta)
        
        # Crear órdenes de contratación de ejemplo
        ordenes = [
            OrdenContratacion(
                cliente="Empresa ABC",
                cargo="Desarrollador Full Stack",
                examenes="Examen técnico, Entrevista, Prueba psicológica"
            ),
            OrdenContratacion(
                cliente="Empresa XYZ",
                cargo="Analista de Datos",
                examenes="Prueba de SQL, Entrevista técnica, Evaluación de portafolio"
            ),
            OrdenContratacion(
                cliente="Startup Tech",
                cargo="DevOps Engineer",
                examenes="Prueba práctica AWS, Entrevista técnica, Evaluación de experiencia"
            ),
            OrdenContratacion(
                cliente="Corporación Digital",
                cargo="Desarrollador Frontend",
                examenes="Prueba de React, Entrevista técnica, Evaluación de código"
            ),
            OrdenContratacion(
                cliente="Tech Solutions",
                cargo="Desarrollador Backend",
                examenes="Prueba de Java, Entrevista técnica, Evaluación de arquitectura"
            )
        ]
        
        for orden in ordenes:
            db.add(orden)
        
        db.commit()
        print(f"✅ Base de datos inicializada exitosamente con {len(candidatos)} candidatos, {len(ofertas)} ofertas, {len(ordenes)} órdenes y {len(ciudades_creadas)} ciudades.")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 