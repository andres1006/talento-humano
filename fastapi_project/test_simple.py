import requests

def test_simple():
    base_url = "http://localhost:8000"
    
    # Probar health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error en health check: {e}")
        return
    
    # Probar clientes
    try:
        response = requests.get(f"{base_url}/api/v1/clientes")
        print(f"GET clientes: {response.status_code}")
        if response.status_code == 200:
            clientes = response.json()
            print(f"Clientes encontrados: {len(clientes)}")
            for cliente in clientes[:3]:  # Mostrar solo los primeros 3
                print(f"  - {cliente['nombre']}")
    except Exception as e:
        print(f"Error en GET clientes: {e}")

if __name__ == "__main__":
    test_simple() 