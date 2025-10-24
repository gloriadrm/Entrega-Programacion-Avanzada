import requests
import json
from typing import Optional, Dict, Any

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "user4@api.com"
USER_PWD = "SecurePass444"                  # Debe tener 8+ caracteres

SIGNUP_DATA = {
    "name": "User4",
    "age": 40,
    "email": USER_EMAIL,
    "password": USER_PWD
}

# --- FUNCIÓN AUXILIAR PARA IMPRIMIR LA RESPUESTA ---
def print_response(step_number: int, title: str, response: requests.Response) -> Optional[Dict[str, Any]]:
    """Función auxiliar para imprimir la respuesta de la API y devolver el JSON."""
    print(f"\n--- {step_number}. {title} ---")
    print(f"Estado: {response.status_code}")
    
    data = None
    try:
        data = response.json()
        print("Respuesta:", json.dumps(data, indent=2))
    except requests.exceptions.JSONDecodeError:
        print("Respuesta (Error sin JSON):", response.text)
        
    print("-" * 30)
    return data
# ----------------------------------------------------

def signup():
    """Crea la cuenta (o verifica si ya existe)."""
    response = requests.post(f"{BASE_URL}/auth/signup", json=SIGNUP_DATA)
    print_response(1, "POST /auth/signup (Crear Usuario)", response)
    
    return response.status_code in [200, 201] or (response.status_code == 400 and "ya está registrado" in response.text)

if __name__ == "__main__":
    print("==================================================")
    print("INICIANDO PRUEBA 1: REGISTRO DE USUARIO")
    print("==================================================")
    signup()
