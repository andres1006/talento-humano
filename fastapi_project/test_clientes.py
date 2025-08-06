import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_clientes():
    print("🧪 Probando rutas de clientes...")
    
    # Probar GET /clientes
    try:
        response = requests.get(f"{BASE_URL}/clientes")
        print(f"✅ GET /clientes - Status: {response.status_code}")
        if response.status_code == 200:
            clientes = response.json()
            print(f"   Clientes encontrados: {len(clientes)}")
            for cliente in clientes:
                print(f"   - {cliente['nombre']} ({cliente['email']})")
    except Exception as e:
        print(f"❌ Error en GET /clientes: {e}")
    
    # Probar POST /clientes
    try:
        nuevo_cliente = {
            "nombre": "Empresa de Prueba",
            "email": "prueba@test.com",
            "telefono": "3001234567",
            "direccion": "Calle de Prueba #123",
            "activo": True
        }
        response = requests.post(f"{BASE_URL}/clientes", json=nuevo_cliente)
        print(f"✅ POST /clientes - Status: {response.status_code}")
        if response.status_code == 200:
            cliente_creado = response.json()
            print(f"   Cliente creado: {cliente_creado['nombre']} (ID: {cliente_creado['id']})")
            
            # Probar PATCH para cambiar estado
            cliente_id = cliente_creado['id']
            response = requests.patch(f"{BASE_URL}/clientes/{cliente_id}/toggle-status")
            print(f"✅ PATCH /clientes/{cliente_id}/toggle-status - Status: {response.status_code}")
            
            # Probar DELETE
            response = requests.delete(f"{BASE_URL}/clientes/{cliente_id}")
            print(f"✅ DELETE /clientes/{cliente_id} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en POST/PATCH/DELETE: {e}")

if __name__ == "__main__":
    test_clientes() 